import 'dart:async';
import 'package:flutter/material.dart';
import 'package:toswe/presentation/screens/store_screen.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen>
    with TickerProviderStateMixin {
  late AnimationController _logoController;
  late Animation<double> _logoAnimation;

  String _displayedText = '';
  final String _fullText = "Nous vendons pour vous";
  int _textIndex = 0;

  @override
  void initState() {
    super.initState();

    // Typing animation
    Timer.periodic(const Duration(milliseconds: 80), (Timer timer) {
      if (_textIndex < _fullText.length) {
        setState(() {
          _displayedText += _fullText[_textIndex];
          _textIndex++;
        });
      } else {
        timer.cancel();
        _logoController.forward();
      }
    });

    // Logo zoom animation
    _logoController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1000),
    );

    _logoAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _logoController, curve: Curves.elasticOut),
    );

    // After animation, go to StoreScreen
    Future.delayed(const Duration(seconds: 4), () {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => const StoreScreen()),
      );
    });
  }

  @override
  void dispose() {
    _logoController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF2D1B14),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              _displayedText,
              style: const TextStyle(
                color: Colors.white,
                fontSize: 20,
                fontStyle: FontStyle.italic,
                fontFamily: 'Playfair Display',
              ),
            ),
            const SizedBox(height: 30),
            ScaleTransition(
              scale: _logoAnimation,
              child: Column(
                children: [
                  Image.asset(
                    'assets/logo-toswe.png',
                    width: 100,
                    height: 100,
                  ),
                  const SizedBox(height: 8),
                  const Text(
                    "Tôswè",
                    style: TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                      fontFamily: 'Playfair Display',
                      color: Color(0xFFF5E6DA),
                    ),
                  )
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
