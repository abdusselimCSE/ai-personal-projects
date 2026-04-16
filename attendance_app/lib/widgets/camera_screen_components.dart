import 'dart:ui';

import 'package:camera/camera.dart';
import 'package:flutter/material.dart';

class CameraScreenAppBar extends StatelessWidget
    implements PreferredSizeWidget {
  const CameraScreenAppBar({super.key, required this.onSettingsPressed});

  final VoidCallback onSettingsPressed;

  @override
  Size get preferredSize => const Size.fromHeight(kToolbarHeight);

  @override
  Widget build(BuildContext context) {
    return AppBar(
      leading: Padding(
        padding: const EdgeInsets.only(left: 16),
        child: Icon(Icons.verified_user, color: Colors.white),
      ),
      title: const Text(
        'Attendance Scanner',
        style: TextStyle(fontWeight: FontWeight.w600, letterSpacing: 1.2),
      ),
      centerTitle: true,
      backgroundColor: Colors.transparent,
      elevation: 0,
      actions: [
        IconButton(
          icon: const Icon(Icons.settings, color: Colors.white),
          onPressed: onSettingsPressed,
        ),
      ],
    );
  }
}

class CameraPreviewLayer extends StatelessWidget {
  const CameraPreviewLayer({
    super.key,
    required this.controller,
    required this.screenSize,
  });

  final CameraController controller;
  final Size screenSize;

  @override
  Widget build(BuildContext context) {
    final Size previewSize =
        controller.value.previewSize ?? const Size(640, 480);
    final double cameraWidth = previewSize.height;
    final double cameraHeight = previewSize.width;

    return SizedBox(
      width: screenSize.width,
      height: screenSize.height,
      child: FittedBox(
        fit: BoxFit.cover,
        child: SizedBox(
          width: cameraWidth,
          height: cameraHeight,
          child: CameraPreview(controller),
        ),
      ),
    );
  }
}

class CameraTopGradientOverlay extends StatelessWidget {
  const CameraTopGradientOverlay({super.key});

  @override
  Widget build(BuildContext context) {
    return Positioned(
      top: 0,
      left: 0,
      right: 0,
      height: 110,
      child: ClipRect(
        child: BackdropFilter(
          filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
          child: Container(
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                colors: [Colors.black87, Colors.transparent],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
