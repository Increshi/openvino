# Copyright (C) 2018-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

import pytest

from pytorch_layer_test_class import PytorchLayerTest, skip_if_export


class TestRRelu(PytorchLayerTest):
    def _prepare_input(self):
        import numpy as np
        return (np.random.randn(1, 3, 224, 224).astype(np.float32),)

    def create_model(self, lower,upper, inplace):
        import torch
        import torch.nn.functional as F

        class aten_rrelu(torch.nn.Module):
            def __init__(self, lower,upper, inplace):
                super(aten_rrelu, self).__init__()
                self.lower = lower
                self.upper = upper
                self.inplace = inplace

            def forward(self, x):
                return x, F.rrelu(x, self.lower,self.upper,inplace=self.inplace)

        ref_net = None

        return aten_rrelu(lower,upper, inplace), ref_net, "aten::rrelu" if not inplace else "aten::rrelu_"

    @pytest.mark.parametrize("lower", [0.125, 0.1, 0.05])
    @pytest.mark.parametrize("upper", [0.333, 0.4, 0.5])
    @pytest.mark.parametrize("inplace", [skip_if_export(True), False])
    @pytest.mark.nightly
    @pytest.mark.precommit
    @pytest.mark.precommit_fx_backend
    def test_rrelu(self, lower,upper, inplace, ie_device, precision, ir_version):
        self._test(*self.create_model(lower,upper, inplace), ie_device, precision, ir_version)

