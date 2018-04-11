import torch
import torch.nn as nn
import torch.nn.functional as F


class SC2QNet(nn.Module):

    def __init__(self,
                 resolution,
                 n_channels_screen,
                 n_channels_minimap,
                 n_out,
                 batchnorm=False):
        super(SC2QNet, self).__init__()
        self.screen_conv1 = nn.Conv2d(in_channels=n_channels_screen,
                                      out_channels=16,
                                      kernel_size=5,
                                      stride=1,
                                      padding=2)
        self.screen_conv2 = nn.Conv2d(in_channels=16,
                                      out_channels=32,
                                      kernel_size=3,
                                      stride=1,
                                      padding=1)
        self.minimap_conv1 = nn.Conv2d(in_channels=n_channels_minimap,
                                       out_channels=16,
                                       kernel_size=5,
                                       stride=1,
                                       padding=2)
        self.minimap_conv2 = nn.Conv2d(in_channels=16,
                                       out_channels=32,
                                       kernel_size=3,
                                       stride=1,
                                       padding=1)
        if batchnorm:
            self.screen_bn1 = nn.BatchNorm2d(16)
            self.screen_bn2 = nn.BatchNorm2d(32)
            self.minimap_bn1 = nn.BatchNorm2d(16)
            self.minimap_bn2 = nn.BatchNorm2d(32)
            self.player_bn = nn.BatchNorm2d(10)
        self.state_fc = nn.Linear(74 * (resolution ** 2), 200)
        self.q_fc = nn.Linear(200, n_out)
        self._batchnorm = batchnorm

    def forward(self, x):
        screen, minimap, player = x
        player = player.clone().repeat(
            screen.size(2), screen.size(3), 1, 1).permute(2, 3, 0, 1)
        if self._batchnorm:
            screen = F.leaky_relu(self.screen_bn1(self.screen_conv1(screen)))
            screen = F.leaky_relu(self.screen_bn2(self.screen_conv2(screen)))
            minimap = F.leaky_relu(self.minimap_bn1(self.minimap_conv1(minimap)))
            minimap = F.leaky_relu(self.minimap_bn2(self.minimap_conv2(minimap)))
            player = self.player_bn(player.contiguous())
        else:
            screen = F.leaky_relu(self.screen_conv1(screen))
            screen = F.leaky_relu(self.screen_conv2(screen))
            minimap = F.leaky_relu(self.minimap_conv1(minimap))
            minimap = F.leaky_relu(self.minimap_conv2(minimap))
        screen_minimap = torch.cat((screen, minimap, player), 1)
        state = F.leaky_relu(self.state_fc(
            screen_minimap.view(screen_minimap.size(0), -1)))
        return self.q_fc(state)


class SC2QNetV2(nn.Module):

    def __init__(self,
                 resolution,
                 n_channels_screen,
                 n_channels_minimap,
                 n_out,
                 batchnorm=False):
        super(SC2QNetV2, self).__init__()
        assert resolution == 32
        self.screen_conv1 = nn.Conv2d(in_channels=n_channels_screen,
                                      out_channels=16,
                                      kernel_size=5,
                                      stride=1,
                                      padding=2)
        self.minimap_conv1 = nn.Conv2d(in_channels=n_channels_minimap,
                                       out_channels=16,
                                       kernel_size=5,
                                       stride=1,
                                       padding=2)
        self.screen_conv2 = nn.Conv2d(in_channels=16,
                                      out_channels=32,
                                      kernel_size=3,
                                      stride=2,
                                      padding=2)
        self.minimap_conv2 = nn.Conv2d(in_channels=16,
                                       out_channels=32,
                                       kernel_size=3,
                                       stride=2,
                                       padding=2)
        if batchnorm:
            self.screen_bn1 = nn.BatchNorm2d(16)
            self.screen_bn2 = nn.BatchNorm2d(32)
            self.minimap_bn1 = nn.BatchNorm2d(16)
            self.minimap_bn2 = nn.BatchNorm2d(32)
        self.spatial_fc = nn.Linear(64 * 17 * 17, 256)
        self.nonspatial_fc1 = nn.Linear(10, 512)
        self.nonspatial_fc2 = nn.Linear(512, 256)
        self.q_fc = nn.Linear(512, n_out)
        self._batchnorm = batchnorm

    def forward(self, x):
        screen, minimap, player = x
        if self._batchnorm:
            screen = F.relu(self.screen_bn1(self.screen_conv1(screen)))
            screen = F.relu(self.screen_bn2(self.screen_conv2(screen)))
            minimap = F.relu(self.minimap_bn1(self.minimap_conv1(minimap)))
            minimap = F.relu(self.minimap_bn2(self.minimap_conv2(minimap)))
        else:
            screen = F.relu(self.screen_conv1(screen))
            screen = F.relu(self.screen_conv2(screen))
            minimap = F.relu(self.minimap_conv1(minimap))
            minimap = F.relu(self.minimap_conv2(minimap))
        screen_minimap = torch.cat((screen, minimap), 1)
        spatial_state = F.relu(self.spatial_fc(
            screen_minimap.view(screen_minimap.size(0), -1)))
        nonspatial_state = F.relu(self.nonspatial_fc2(
            F.relu(self.nonspatial_fc1(player))))
        state = torch.cat((spatial_state, nonspatial_state), 1)
        return self.q_fc(state)


class SC2DuelingQNetV2(nn.Module):

    def __init__(self,
                 resolution,
                 n_channels_screen,
                 n_channels_minimap,
                 n_out,
                 batchnorm=False):
        super(SC2DuelingQNetV2, self).__init__()
        assert resolution == 32
        self.screen_conv1 = nn.Conv2d(in_channels=n_channels_screen,
                                      out_channels=16,
                                      kernel_size=5,
                                      stride=1,
                                      padding=2)
        self.minimap_conv1 = nn.Conv2d(in_channels=n_channels_minimap,
                                       out_channels=16,
                                       kernel_size=5,
                                       stride=1,
                                       padding=2)
        self.screen_conv2 = nn.Conv2d(in_channels=16,
                                      out_channels=32,
                                      kernel_size=3,
                                      stride=2,
                                      padding=2)
        self.minimap_conv2 = nn.Conv2d(in_channels=16,
                                       out_channels=32,
                                       kernel_size=3,
                                       stride=2,
                                       padding=2)
        if batchnorm:
            self.screen_bn1 = nn.BatchNorm2d(16)
            self.screen_bn2 = nn.BatchNorm2d(32)
            self.minimap_bn1 = nn.BatchNorm2d(16)
            self.minimap_bn2 = nn.BatchNorm2d(32)

        self.value_sp_fc = nn.Linear(64 * 17 * 17, 256)
        self.value_nonsp_fc1 = nn.Linear(10, 512)
        self.value_nonsp_fc2 = nn.Linear(512, 256)
        self.value_final_fc = nn.Linear(512, 1)

        self.adv_sp_fc = nn.Linear(64 * 17 * 17, 256)
        self.adv_nonsp_fc1 = nn.Linear(10, 512)
        self.adv_nonsp_fc2 = nn.Linear(512, 256)
        self.adv_final_fc = nn.Linear(512, n_out)
        self._batchnorm = batchnorm

    def forward(self, x):
        screen, minimap, player = x
        if self._batchnorm:
            screen = F.relu(self.screen_bn1(self.screen_conv1(screen)))
            screen = F.relu(self.screen_bn2(self.screen_conv2(screen)))
            minimap = F.relu(self.minimap_bn1(self.minimap_conv1(minimap)))
            minimap = F.relu(self.minimap_bn2(self.minimap_conv2(minimap)))
        else:
            screen = F.relu(self.screen_conv1(screen))
            screen = F.relu(self.screen_conv2(screen))
            minimap = F.relu(self.minimap_conv1(minimap))
            minimap = F.relu(self.minimap_conv2(minimap))
        screen_minimap = torch.cat((screen, minimap), 1)
        screen_minimap = screen_minimap.view(screen_minimap.size(0), -1)

        value_sp_state = F.relu(self.value_sp_fc(screen_minimap))
        value_nonsp_state = F.relu(self.value_nonsp_fc2(
            F.relu(self.value_nonsp_fc1(player))))
        value_state = torch.cat((value_sp_state, value_nonsp_state), 1)
        value = self.value_final_fc(value_state)

        adv_sp_state = F.relu(self.adv_sp_fc(screen_minimap))
        adv_nonsp_state = F.relu(self.adv_nonsp_fc2(
            F.relu(self.adv_nonsp_fc1(player))))
        adv_state = torch.cat((adv_sp_state, adv_nonsp_state), 1)
        adv = self.adv_final_fc(adv_state)
        adv_subtract = adv - adv.mean(dim=1, keepdim=True)
        return value + adv_subtract


class SC2NonSpatialQNet(nn.Module):
    def __init__(self,
                 in_dims,
                 out_dims,
                 batchnorm=False):
        super(SC2NonSpatialQNet, self).__init__()
        self.fc1 = nn.Linear(in_dims, 1024)
        self.fc2 = nn.Linear(1024, 512)
        self.fc3 = nn.Linear(512, 256)
        self.fc4 = nn.Linear(256, out_dims)
        if batchnorm:
            self.bn1 = nn.BatchNorm1d(1024)
            self.bn2 = nn.BatchNorm1d(512)
            self.bn3 = nn.BatchNorm1d(256)
        self._batchnorm = batchnorm

    def forward(self, inputs):
        x = inputs
        if not self._batchnorm:
            x = F.relu(self.fc1(x))
            x = F.relu(self.fc2(x))
            x = F.relu(self.fc3(x))
            x = F.relu(self.fc4(x))
        else:
            x = F.relu(self.bn1(self.fc1(x)))
            x = F.relu(self.bn2(self.fc2(x)))
            x = F.relu(self.bn3(self.fc3(x)))
            x = F.relu(self.fc4(x))
        return x


class SC2DuelingQNetV3(nn.Module):

    def __init__(self,
                 resolution,
                 n_channels,
                 n_dims,
                 n_out,
                 batchnorm=False):
        super(SC2DuelingQNetV3, self).__init__()
        assert resolution == 32
        self.conv1 = nn.Conv2d(in_channels=n_channels,
                               out_channels=32,
                               kernel_size=5,
                               stride=1,
                               padding=2)
        self.conv2 = nn.Conv2d(in_channels=32,
                               out_channels=32,
                               kernel_size=3,
                               stride=2,
                               padding=2)
        self.conv3 = nn.Conv2d(in_channels=32,
                               out_channels=16,
                               kernel_size=3,
                               stride=3,
                               padding=2)
        if batchnorm:
            self.bn1 = nn.BatchNorm2d(32)
            self.bn2 = nn.BatchNorm2d(32)
            self.bn3 = nn.BatchNorm2d(16)

        self.value_sp_fc = nn.Linear(16 * 7 * 7, 256)
        self.value_nonsp_fc1 = nn.Linear(n_dims, 1024)
        self.value_nonsp_fc2 = nn.Linear(1024, 512)
        self.value_nonsp_fc3 = nn.Linear(512, 256)
        self.value_final_fc = nn.Linear(512, 1)

        self.adv_sp_fc = nn.Linear(16 * 7 * 7, 256)
        self.adv_nonsp_fc1 = nn.Linear(n_dims, 1024)
        self.adv_nonsp_fc2 = nn.Linear(1024, 512)
        self.adv_nonsp_fc3 = nn.Linear(512, 256)
        self.adv_final_fc = nn.Linear(512, n_out)
        self._batchnorm = batchnorm

    def forward(self, x):
        spatial, nonspatial = x
        if self._batchnorm:
            spatial = F.relu(self.bn1(self.conv1(spatial)))
            spatial = F.relu(self.bn2(self.conv2(spatial)))
            spatial = F.relu(self.bn3(self.conv3(spatial)))
        else:
            spatial = F.relu(self.conv1(spatial))
            spatial = F.relu(self.conv2(spatial))
            spatial = F.relu(self.conv3(spatial))
        spatial = spatial.view(spatial.size(0), -1)

        value_sp_state = F.relu(self.value_sp_fc(spatial))
        value_nonsp_state = F.relu(self.value_nonsp_fc1(nonspatial))
        value_nonsp_state = F.relu(self.value_nonsp_fc2(value_nonsp_state))
        value_nonsp_state = F.relu(self.value_nonsp_fc3(value_nonsp_state))
        value_state = torch.cat((value_sp_state, value_nonsp_state), 1)
        value = self.value_final_fc(value_state)

        adv_sp_state = F.relu(self.adv_sp_fc(spatial))
        adv_nonsp_state = F.relu(self.adv_nonsp_fc1(nonspatial))
        adv_nonsp_state = F.relu(self.adv_nonsp_fc2(adv_nonsp_state))
        adv_nonsp_state = F.relu(self.adv_nonsp_fc3(adv_nonsp_state))
        adv_state = torch.cat((adv_sp_state, adv_nonsp_state), 1)
        adv = self.adv_final_fc(adv_state)
        adv_subtract = adv - adv.mean(dim=1, keepdim=True)
        return value + adv_subtract
