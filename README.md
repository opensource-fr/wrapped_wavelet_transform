# Wavelet Transform

[image](./docs/gtkwave_of_wt.png)

This repo has a wavelet transform targeting a stream of 8-bit inputs.

See following sections for usage and details about the transform.

## Usage: Clocking in Input Bytes and Reading Output Byes

### Clocking in Input Bytes

1. Set up 8-bits on 8 gpios (the `i_value` inputs).
2. "clock-in" these values by creating a rising edge of the `i_data_clk` signal.

NOTE: all filters complete the computation after one clock cycle.

### Reading out Output Bytes

1. Set `o_select_output_channel` gpios to desired filter for readout
2. Wait a couple cycles (crossing clock domains)
3. Read the 8-bits (in parallel) from `o_multiplexed_wavelet_out`

## Process for scaling up the transform

Scaling up to cover a larger range of input frequencies involves:

1. In `wavelet_transform`.v: add new fir module with the parameters from `WT.py` (see next section)
2. In `wavelet_transform`.v: incrementing `TOTAL_FILTERS` parameter
3. In `wavelet_transform`.v: update the `TOTAL_TAPS` parameter (# bits in largest filter)

### Generating parameters from WT.py

To help with the math of scaling up the transform, use the following python script located at the follwing path:

```
.
└── wavelet_transform
    └── py
        └── WT.py
```

Change the parameters for generating the new `Wavelet_Array` object.

For example increasing from the default 8 filters to 16:

```python
wa = Wavelet_Array(base_num_elem=3, max_wavelet_order=16)
```
Next, print the filter element values in either decimal or hex (two's
complement) representation:
```python
wa.print_all_filters() # decimal representation
wa.print_all_filters_hex() # hex representation
```

## Some Interesting Wavelet Properties

The 1-D wavelet transform can be seen as an alternative to the FT transform on time-series data.

Essentially it's a convolution of a small wave or 'wavelet'.

Typically, the shape of the wavelet is the same for each of ranges of interest,
just scaled, making construction of the transform two steps:

1. Base wavelet equation (this repo uses the Ricker Wavelet family of wavelets)
2. Scaling of the wavelet to larger size (smaller frequencies)

### Wavelets Retain Phase Data

With wavelet's one sees not just the intensity of frequency, but whether high or low at that point in time.

This is very interesting to monitoring and especially extrapolating patterns in data.

### Wavelets Increase Temporal Resolution (when compared to Fourier Transform)

Unlike the fft (which uses same time scale for multiple frequencies), each
frequency range has very high temporal localization.

This also means different resolution between different frequencies, higher frequencies
will have higher temporal resolution.

Will be better or at par with temporal resolution than the fourier frequency transform.

# Zero to ASIC Course

This project was made as part of the [Zero to ASIC Course](https://zerotoasiccourse.com)!

# License

This project is [licensed under Apache 2](LICENSE)
