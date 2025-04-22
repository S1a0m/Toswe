import 'dart:async';
import 'dart:ui';
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
  final String _fullText = "Nous vendons pour vous.";
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
    return Container(
      decoration: const BoxDecoration(
        gradient: RadialGradient(
          center: Alignment.center,
          radius: 0.85,
          colors: [
            Color(0xFF7D260F),
            Color(0xFF2D1B14),
          ],
          stops: [0.08, 1.0],
        ),
      ),
      child: Stack(
        children: [
          // 🎨 Image de fond
          Container(
            decoration: const BoxDecoration(
              image: DecorationImage(
                image: AssetImage("assets/toswe-africa-art.png"),
                fit: BoxFit.cover,
              ),
            ),
          ),

          // 💎 Flou général
          BackdropFilter(
            filter: ImageFilter.blur(sigmaX: 8, sigmaY: 8),
            child: Container(
              color: Colors.black.withOpacity(0),
            ),
          ),

          // 📋 Contenu
          SafeArea(
            child: Scaffold(
              backgroundColor: Colors.transparent,
              body: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(
                      _displayedText,
                      style: const TextStyle(
                        color: Color.fromRGBO(245, 230, 218, 0.5),
                        fontSize: 30,
                        // fontStyle: FontStyle.italic,
                        fontFamily: 'Playfair Display',
                        fontWeight: FontWeight.w100,
                      ),
                    ),
                    const SizedBox(height: 30),
                    ScaleTransition(
                      scale: _logoAnimation,
                      child: Column(
                        children: [
                          /*Image.asset(
                        'assets/icon/Tw5_1.png',
                        width: 200,
                        height: 200,
                      ),*/
                          Image.asset('assets/icon/Tw7_2.png',
                              width: 200, height: 80),
                          const SizedBox(height: 8),
                          /*const Text(
                        "Tôswè",
                        style: TextStyle(
                          fontSize: 35,
                          fontWeight: FontWeight.bold,
                          fontFamily: 'Playfair Display',
                          color: Color(0xFFBE7C6A),
                        ),
                      )*/
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

/**
 * Scaffold(
        backgroundColor: const Color.fromARGB(100, 125, 38, 15),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                _displayedText,
                style: const TextStyle(
                  color: Color.fromRGBO(245, 230, 218, 0.5),
                  fontSize: 30,
                  // fontStyle: FontStyle.italic,
                  fontFamily: 'Playfair Display',
                  fontWeight: FontWeight.w100,
                ),
              ),
              const SizedBox(height: 30),
              ScaleTransition(
                scale: _logoAnimation,
                child: Column(
                  children: [
                    /*Image.asset(
                      'assets/icon/Tw5_1.png',
                      width: 200,
                      height: 200,
                    ),*/
                    Image.asset('assets/icon/Tw7_2.png', width: 200, height: 80),
                    const SizedBox(height: 8),
                    /*const Text(
                      "Tôswè",
                      style: TextStyle(
                        fontSize: 35,
                        fontWeight: FontWeight.bold,
                        fontFamily: 'Playfair Display',
                        color: Color(0xFFBE7C6A),
                      ),
                    )*/
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
 */
