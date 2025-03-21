import torch
import torch.nn as nn
import torch.nn.functional as F


class Resample2d(nn.Module):
    def __init__(self, kernel_size=1, bilinear=True):
        super(Resample2d, self).__init__()
        self.kernel_size = kernel_size  # Not used in this version
        self.bilinear = bilinear        # If False, will use nearest neighbor

    def forward(self, input1, flow):
        """
        input1: (B, C, H, W) - input feature map
        flow: (B, 2, H, W) - optical flow (x, y) per pixel
        """
        B, C, H, W = input1.size()

        # Create base grid
        y_grid, x_grid = torch.meshgrid(
            torch.arange(H, device=input1.device),
            torch.arange(W, device=input1.device),
            indexing='ij'
        )
        base_grid = torch.stack((x_grid, y_grid), dim=2)  # (H, W, 2)
        base_grid = base_grid.unsqueeze(0).repeat(B, 1, 1, 1).float()  # (B, H, W, 2)

        flow = flow.permute(0, 2, 3, 1)  # (B, H, W, 2)
        sampling_grid = base_grid + flow

        # Normalize to [-1, 1]
        sampling_grid[..., 0] = 2.0 * sampling_grid[..., 0] / max(W - 1, 1) - 1.0
        sampling_grid[..., 1] = 2.0 * sampling_grid[..., 1] / max(H - 1, 1) - 1.0

        # Sample using bilinear or nearest interpolation
        mode = 'bilinear' if self.bilinear else 'nearest'
        output = F.grid_sample(input1, sampling_grid, mode=mode, align_corners=True, padding_mode='border')

        return output
