import 'package:flutter/material.dart';
import 'package:toswe/presentation/screens/notification.dart';
// import 'package:toswe/presentation/screens/profil.dart';
import 'package:toswe/presentation/screens/search.dart';
import 'package:toswe/presentation/screens/splash_screen.dart';
// import 'package:toswe/presentation/screens/settings.dart';
import '../screens/store_screen.dart';
import '../screens/login_screen.dart';

class AppRoutes {
  static const String initial = '/splash';

  static final Map<String, WidgetBuilder> routes = {
    '/login': (_) => const LoginScreen(),
    '/store': (_) => const StoreScreen(),
    /*'/profile': (_) => const ProfilScreen(),
    '/settings': (_) => const SettingsScreen(),*/
    '/notifications': (_) => const NotificationScreen(),
    '/search': (_) => const SearchScreen(),
    '/splash': (_) => const SplashScreen(),
  };
}
