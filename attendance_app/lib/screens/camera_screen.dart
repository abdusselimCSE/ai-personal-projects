import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../main.dart' show cameras;
import '../services/api_service.dart';
import '../widgets/camera_controls.dart';
import '../widgets/camera_screen_components.dart';
import '../widgets/scan_result_dialog.dart';
import '../widgets/scanning_overlay.dart';
import '../widgets/server_settings_sheet.dart';

class CameraScreen extends StatefulWidget {
  const CameraScreen({super.key});

  @override
  State<CameraScreen> createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen>
    with SingleTickerProviderStateMixin {
  CameraController? _controller;
  bool _isCameraInitialized = false;
  bool _isScanning = false;
  String _serverIp = "192.168.1.100";

  late AnimationController _animController;
  late Animation<double> _pulseAnimation;

  @override
  void initState() {
    super.initState();
    _animController = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 1),
    )..repeat(reverse: true);
    _pulseAnimation = Tween<double>(begin: 0.8, end: 1.1).animate(
      CurvedAnimation(parent: _animController, curve: Curves.easeInOut),
    );

    _loadServerIp();
    if (cameras.isNotEmpty) {
      _initCamera(cameras.first);
    }
  }

  Future<void> _loadServerIp() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      _serverIp = prefs.getString('server_ip') ?? _serverIp;
    });
  }

  Future<void> _saveServerIp(String ip) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('server_ip', ip);
    setState(() {
      _serverIp = ip;
    });
  }

  Future<void> _initCamera(CameraDescription description) async {
    final CameraController cameraController = CameraController(
      description,
      ResolutionPreset.high,
      enableAudio: false,
    );
    _controller = cameraController;

    try {
      await cameraController.initialize();
      setState(() {
        _isCameraInitialized = true;
      });
    } catch (e) {
      debugPrint("Camera init error: $e");
    }
  }

  @override
  void dispose() {
    _controller?.dispose();
    _animController.dispose();
    super.dispose();
  }

  Future<void> _showSettings() async {
    await showServerSettingsSheet(
      context: context,
      initialIp: _serverIp,
      onSave: _saveServerIp,
    );
  }

  void _showResultDialog(
    String title,
    String message,
    IconData icon,
    Color color,
  ) {
    showScanResultDialog(
      context: context,
      title: title,
      message: message,
      icon: icon,
      color: color,
    );
  }

  void _handleRecognitionResponse(Map<String, dynamic> jsonResponse) {
    if (jsonResponse["status"] != "success") {
      _showResultDialog(
        "Error",
        jsonResponse["message"]?.toString() ?? "An unknown error",
        Icons.error,
        Colors.red,
      );
      return;
    }

    final dynamic facesData = jsonResponse["faces"];
    if (facesData is! List || facesData.isEmpty) {
      _showResultDialog(
        "No Face Found",
        "We couldn't see a face. Please align your face in the camera.",
        Icons.face,
        Colors.grey,
      );
      return;
    }

    final dynamic firstFace = facesData.first;
    final String name = firstFace["name"]?.toString() ?? "Unknown";
    final String status = firstFace["status"]?.toString() ?? "";
    _showFaceStatusResult(name: name, status: status);
  }

  void _showFaceStatusResult({required String name, required String status}) {
    if (name == "Unknown") {
      _showResultDialog(
        "Access Denied",
        "Face not recognized. Please add yours to the database.",
        Icons.error_outline,
        Colors.redAccent,
      );
      return;
    }

    if (status == "ALREADY_LOGGED") {
      _showResultDialog(
        "Already Present",
        "Hi $name, you have already been marked present today!",
        Icons.waving_hand,
        Colors.blueAccent,
      );
      return;
    }

    if (status == "COOLDOWN") {
      _showResultDialog(
        "Hang on",
        "Please wait a moment before scanning again.",
        Icons.timer,
        Colors.orangeAccent,
      );
      return;
    }

    _showResultDialog(
      "Access Granted",
      "Attendance logged for $name. Have a great day!",
      Icons.check_circle_outline,
      Colors.greenAccent,
    );
  }

  Future<void> _scanAttendance() async {
    if (_controller == null || !_isCameraInitialized || _isScanning) return;

    setState(() {
      _isScanning = true;
    });

    try {
      final XFile picture = await _controller!.takePicture();
      final Map<String, dynamic> jsonResponse =
          await ApiService.sendImageForRecognition(_serverIp, picture.path);
      _handleRecognitionResponse(jsonResponse);
    } catch (e) {
      _showResultDialog(
        "Network Error",
        "Could not reach $_serverIp:8000. Make sure the backend server is running and on the same Wi-Fi. Details: $e",
        Icons.cloud_off,
        Colors.red,
      );
    } finally {
      if (mounted) {
        setState(() {
          _isScanning = false;
        });
      }
    }
  }

  void _flipCamera() {
    if (_controller == null || cameras.length < 2) return;
    int currentIndex = cameras.indexOf(_controller!.description);
    int newIndex = (currentIndex + 1) % cameras.length;
    setState(() {
      _isCameraInitialized = false;
    });
    _initCamera(cameras[newIndex]);
  }

  @override
  Widget build(BuildContext context) {
    if (!_isCameraInitialized) {
      return const Scaffold(
        backgroundColor: Colors.black,
        body: Center(
          child: CircularProgressIndicator(color: Color(0xFF6C63FF)),
        ),
      );
    }

    final Size size = MediaQuery.of(context).size;
    final CameraController controller = _controller!;

    return Scaffold(
      backgroundColor: Colors.black,
      extendBodyBehindAppBar: true,
      appBar: CameraScreenAppBar(onSettingsPressed: _showSettings),
      body: Stack(
        fit: StackFit.expand,
        children: [
          CameraPreviewLayer(controller: controller, screenSize: size),
          const CameraTopGradientOverlay(),
          if (_isScanning) ScanningOverlay(pulseAnimation: _pulseAnimation),
          CameraControls(onScan: _scanAttendance, onFlip: _flipCamera),
        ],
      ),
    );
  }
}
