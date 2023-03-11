#!/usr/bin/env python

"""Tests for `qfieldlayout` package."""

from qfieldlayout.qlayout import add_field
import numpy as np
from timeit import default_timer as timer


def test_add_field_positions(small_size=21, large_size=101):
    # large target, small source
    test_add_field_overlaps(small_size, large_size)
    # small target, large source
    test_add_field_overlaps(large_size, small_size)


def test_add_field(source_size, target_size, pos="center", dtype=np.int16):
    source = np.ones((source_size, source_size), dtype=dtype)
    target = np.ones((target_size, target_size), dtype=dtype)
    target_max_x = target.shape[0] - 1
    target_max_y = target.shape[1] - 1
    target_center_x = int(target.shape[0] / 2)
    target_center_y = int(target.shape[1] / 2)
    print(source.shape, target.shape, " ", pos)
    if pos == "top_left":
        add_field(source, target, 0, 0)
    elif pos == "bottom_right":
        add_field(source, target, target_max_x, target_max_y)
    elif pos == "center":
        add_field(source, target, target_center_x, target_center_y)


def test_add_field_overlaps(source_size, target_size):
    test_add_field(source_size, target_size, pos="top_left")
    test_add_field(source_size, target_size, pos="bottom_right")
    test_add_field(source_size, target_size, pos="center")


def test_add_field_speed(target_size, source_size, rounds=1000, target_x=5, target_y=5, dtype=np.int16):
    target_field = np.ones((target_size, target_size), dtype=dtype)
    source_field = np.ones((source_size, target_size), dtype=dtype)
    start = timer()
    for i in range(0, rounds):
        add_field(source_field, target_field, target_x, target_y)
    end = timer()
    elapsed_time = end - start
    # rate = elapsed_time / rounds
    # print("Elapsed time = ", elapsed_time , " for ", rounds, " rounds. Rate = ", rate, " per round")
    # print(f'Elapsed time = {elapsed_time:.3f}')
    print(f'{rounds} rounds at {elapsed_time / rounds:.6f}/second in {elapsed_time:.3f} seconds')


test_add_field_overlaps(21, 101)
test_add_field_speed(101, 21)
