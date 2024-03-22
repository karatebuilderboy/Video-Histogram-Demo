import cv2
import numpy as np
import os
from joblib import Parallel, delayed
import time

def match_channel(source_channel, reference_channel):
    start_time = time.time()
    src_values, bin_idx, src_counts = np.unique(source_channel, return_inverse=True, return_counts=True)
    ref_values, ref_counts = np.unique(reference_channel, return_counts=True)
    src_quantiles = np.cumsum(src_counts).astype(np.float64) / source_channel.size
    ref_quantiles = np.cumsum(ref_counts).astype(np.float64) / reference_channel.size
    interp_values = np.interp(src_quantiles, ref_quantiles, ref_values)
    end_time = time.time()
    return interp_values[bin_idx].reshape(source_channel.shape), end_time - start_time

def histogram_match(source, reference):
    source_channels = cv2.split(source)
    reference_channels = cv2.split(reference)
    results = Parallel(n_jobs=3)(delayed(match_channel)(source_channels[channel], reference_channels[channel]) for channel in range(3))
    matched_channels = [result[0] for result in results]
    times = [result[1] for result in results]
    matched = cv2.merge(matched_channels)
    return matched, times

def process_video(video_path, reference_image_path, log_path):
    reference = cv2.imread(reference_image_path)
    cap = cv2.VideoCapture(video_path)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_path = os.path.join(os.path.dirname(video_path), "processed_video_color_parallel.mp4")
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height), True)
    previous_frame = None
    log_entries = []
    total_start_time = time.time()
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if previous_frame is None:
            processed_frame, times = histogram_match(frame, reference)
        else:
            matched_to_previous, times_previous = histogram_match(frame, previous_frame)
            matched_to_reference, times_reference = histogram_match(frame, reference)
            processed_frame = ((matched_to_previous.astype(np.float32) + matched_to_reference.astype(np.float32)) / 2).astype(np.uint8)
            times = [tp + tr for tp, tr in zip(times_previous, times_reference)]
        previous_frame = processed_frame
        out.write(processed_frame)
        log_entry = f"Frame processing times (R, G, B): {times}"
        print(log_entry)
        log_entries.append(log_entry)
    total_end_time = time.time()
    total_time_log = f"Total processing time: {total_end_time - total_start_time} seconds"
    print(total_time_log)
    log_entries.append(total_time_log)
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    with open(log_path, 'w') as f:
        f.write('\n'.join(log_entries))
    print(f"Processed video has been saved to: {output_path}")
    print(f"Log has been saved to: {log_path}")

video_path = 'testfootage.mp4'
reference_image_path = 'testreference.png'
log_path = 'log.txt'
process_video(video_path, reference_image_path, log_path)
