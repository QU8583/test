import shutil

import numpy as np
import librosa

import tkinter as tk
from tkinter import filedialog
import os







def detect_audio_peaks(file):

    samples, sample_rate = librosa.load(file, sr=None, mono=True)

    # RMS,归一化
    rms = librosa.feature.rms(y=samples, frame_length=1024, hop_length=512)[0]
    rms_normalized = (rms - rms.min()) / (rms.max() - rms.min())

    # 检测峰值
    peak_indices = librosa.util.peak_pick(
        rms_normalized,
        pre_max=3, post_max=3,
        pre_avg=3, post_avg=5,
        delta=0.05, wait=100
    )
    # 将样本索引转换为秒
    peak_times = [(512 * i) / sample_rate for i in peak_indices]





    for i in range(len(peak_times)):
      jia = peak_times[i]
      float(jia)
      jia = format(jia,'.2f')
      peak_times[i] = jia
    with open('use.txt', 'w', encoding='utf-8') as file:
      for i in range(len(peak_times)):
          if i == 0:
              t = peak_times[i]

          else:
              t = float(peak_times[i]) - float(peak_times[i - 1])
              t = format(t, '.2f')
          t = float(t) * 1000
          t = int(t)
          t = str(t)
          file.write('1,' + t + "\n")
    return peak_times






