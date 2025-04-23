import 'dart:ui';
import 'package:flutter/material.dart';

class SearchScreen extends StatelessWidget {
  const SearchScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(
        gradient: RadialGradient(
          center: Alignment.center,
          radius: 0.85,
          colors: [Color(0xFF7D260F), Color(0xFF2D1B14)],
          stops: [0.08, 1.0],
        ),
      ),
      child: Scaffold(
        backgroundColor: Colors.transparent,
        appBar: AppBar(
          title: _SearchBar(),
          centerTitle: true,
          //automaticallyImplyLeading: false,
          flexibleSpace: ClipRect(
            child: BackdropFilter(
              filter: ImageFilter.blur(sigmaX: 15.0, sigmaY: 15.0),
              child: Container(
                color: const Color.fromRGBO(245, 230, 218, 0.4),
              ),
            ),
          ),
          elevation: 0,
          backgroundColor: Colors.transparent,
          // leadingWidth: 150,
          /*leading: Padding(
            padding: const EdgeInsets.all(8.0),
            child: Row(
              children: [
                Image.asset('assets/icon/Tw7_2.png', width: 100, height: 50),
              ],
            ),
          ),*/
        ),
        body: Stack(
          children: [
            Container(
              decoration: const BoxDecoration(
                image: DecorationImage(
                  image: AssetImage("assets/toswe-africa-art.png"),
                  fit: BoxFit.cover,
                ),
              ),
            ),
            BackdropFilter(
              filter: ImageFilter.blur(sigmaX: 8, sigmaY: 8),
              child: Container(
                color: Colors.black.withOpacity(0),
              ),
            ),
            SafeArea(
              child: const Center(
                child: Text(
                  'Recherche en cours...',
                  style: TextStyle(color: Colors.white, fontSize: 18),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _SearchBar extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(30),
      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaX: 6, sigmaY: 6),
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 16),
          height: 45,
          decoration: BoxDecoration(
            color: const Color.fromRGBO(255, 255, 255, 0.2),
            borderRadius: BorderRadius.circular(30),
            border: Border.all(
              color: const Color(0xFF7D260F),
              width: 1.5,
            ),
          ),
          child: const Row(
            children: [
              Icon(Icons.search, color: Color(0xFF2D1B14)),
              SizedBox(width: 10),
              Expanded(
                child: TextField(
                  style: TextStyle(color: Colors.white),
                  decoration: InputDecoration(
                    hintText: 'Rechercher un produit',
                    hintStyle: TextStyle(
                      color: Color.fromRGBO(255, 255, 255, 0.7),
                      fontStyle: FontStyle.italic,
                    ),
                    border: InputBorder.none,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
