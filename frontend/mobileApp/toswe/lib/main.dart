import 'package:flutter/material.dart';
import 'presentation/routes/app_routes.dart';
import 'config/app_theme.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Tôswè',
      theme: AppTheme.lightTheme,
      debugShowCheckedModeBanner: false,
      initialRoute: AppRoutes.initial,
      routes: AppRoutes.routes,
    );
  }
}
