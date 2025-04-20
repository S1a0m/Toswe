import 'package:flutter/material.dart';

class AppTheme {
  static const Color _primaryColor = Color(0xFF7D260F);
  static const Color _backgroundColor = Color(0xFFF5E6DA);

  static final ThemeData lightTheme = ThemeData(
    primaryColor: _primaryColor,
    scaffoldBackgroundColor: _backgroundColor,
    fontFamily: 'Roboto',
    iconTheme: const IconThemeData(color: _primaryColor),
    textTheme: const TextTheme().apply(bodyColor: _primaryColor),
    appBarTheme: const AppBarTheme(
      backgroundColor: _backgroundColor,
      iconTheme: IconThemeData(color: _primaryColor),
    ),
    bottomNavigationBarTheme: const BottomNavigationBarThemeData(
      backgroundColor: _backgroundColor,
      selectedItemColor: Color(0xFFC0A080),
      unselectedItemColor: _primaryColor,
      showUnselectedLabels: true,
    ),
  );
}
