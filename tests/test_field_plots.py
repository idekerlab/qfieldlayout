#!/usr/bin/env python

"""Tests for `qfieldlayout` package."""


import unittest

from qfieldlayout import layout
import matplotlib.pyplot as plt
import seaborn as sns


def save_plot(field, filename="temp_plot.ping"):
    center_x = int(field.shape[0] / 2)
    plt.plot(field[center_x])
    plt.savefig(filename)
    plt.clf()


def save_heatmap(field, filename="temp_heatmap"):
    sns.heatmap(field)
    plt.savefig(filename)
    plt.clf()

class TestQfieldlayout(unittest.TestCase):
    """Tests for `qfieldlayout` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        save_plot(layout.repulsion_field(10, scale=10), "test_repulsion_plot.png")
        save_heatmap(layout.repulsion_field(10, scale=10), "test_repulsion_heatmap.png")
        save_plot(layout.attraction_field(10, scale=5), "test_attraction_plot.png")
        save_heatmap(layout.attraction_field(10, scale=5), "test_attraction_heatmap.png")


