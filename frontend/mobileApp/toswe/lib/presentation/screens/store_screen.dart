import 'package:flutter/material.dart';
import 'package:toswe/presentation/screens/cart_screen.dart';
import 'package:toswe/presentation/screens/notification_screen.dart';
import 'package:toswe/presentation/screens/search_screen.dart';
import './views/store_view.dart';
import './views/profile_view.dart';
import './views/settings_view.dart';
import 'package:url_launcher/url_launcher.dart';
import 'dart:ui';

class StoreScreen extends StatefulWidget {
  const StoreScreen({super.key});

  @override
  State<StoreScreen> createState() => _StoreScreenState();
}

class _StoreScreenState extends State<StoreScreen> {
  int _selectedIndex = 0;

  final Color primaryColor = const Color(0xFF2D1B14);
  final Color activeColor = const Color(0xFF7D260F);

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
      child: Container(
        decoration: const BoxDecoration(
            /*image: DecorationImage(
            image: AssetImage("assets/toswe-africa-art.png"),
            fit: BoxFit.cover,
          ),*/
            ),
        child: Scaffold(
          backgroundColor: Colors.transparent,
          appBar: _buildAppBar(context),
          body: AnimatedSwitcher(
            duration: const Duration(milliseconds: 300),
            transitionBuilder: (Widget child, Animation<double> animation) {
              return FadeTransition(
                opacity: animation,
                child: child,
              );
            },
            child: _getSelectedView(_selectedIndex),
          ),
          floatingActionButton: _selectedIndex == 0
              ? FloatingActionButton(
                  backgroundColor: const Color(0xFF2D1B14),
                  child:
                      const Icon(Icons.shopping_cart, color: Color(0xFFC0A080)),
                  onPressed: () {
                    Navigator.push(context,
                        MaterialPageRoute(builder: (context) {
                      return CartScreen();
                    }));
                  },
                )
              : null,
          bottomNavigationBar: _buildBottomBar(),
        ),
      ),
    );
  }

  Widget _getSelectedView(int index) {
    switch (index) {
      case 0:
        return const StoreView(key: ValueKey('store'));
      case 1:
        return const ProfileView(key: ValueKey('profile'));
      case 2:
        return const SettingsView(key: ValueKey('settings'));
      default:
        return const StoreView(key: ValueKey('default'));
    }
  }
// À mettre en haut du fichier

  AppBar _buildAppBar(BuildContext context) {
    return AppBar(
      automaticallyImplyLeading: false,
      title: Text("Tôswè", style: TextStyle(color: Color(0xFF7D260F))),
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
      // leadingWidth: 68,
      /*leading: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Row(
          children: [
            Image.asset('assets/icon/Tw5_1.png', width: 50, height: 50),
          ],
        ),
      ),*/
      actions: [
        Container(
          margin: const EdgeInsets.symmetric(vertical: 6, horizontal: 10),
          padding: const EdgeInsets.symmetric(horizontal: 4),
          decoration: BoxDecoration(
            color: Colors.white.withOpacity(0.25),
            borderRadius: BorderRadius.circular(16),
          ),
          child: Row(
            children: [
              IconButton(
                icon: const Icon(Icons.notifications_none,
                    color: Color(0xFF2D1B14)),
                onPressed: () {
                  Navigator.push(context,
                      MaterialPageRoute(builder: (_) => NotificationScreen()));
                },
              ),
              IconButton(
                icon: const Icon(Icons.search, color: Color(0xFF2D1B14)),
                onPressed: () {
                  Navigator.push(context,
                      MaterialPageRoute(builder: (_) => SearchScreen()));
                },
              ),
              PopupMenuButton<String>(
                icon: const Icon(Icons.more_vert, color: Color(0xFF2D1B14)),
                color: const Color.fromRGBO(245, 230, 218, 0.9),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
                onSelected: (value) {
                  switch (value) {
                    case 'logout':
                      Navigator.pushReplacementNamed(context, '/login');
                      break;
                    case 'about':
                      _launchURL('https://example.com/a-propos');
                      break;
                    case 'terms':
                      _launchURL('https://example.com/conditions');
                      break;
                  }
                },
                itemBuilder: (context) => [
                  const PopupMenuItem(
                    value: 'logout',
                    child: ListTile(
                      leading: Icon(Icons.logout, color: Color(0xFF7D260F)),
                      title: Text('Déconnexion'),
                    ),
                  ),
                  const PopupMenuItem(
                    value: 'about',
                    child: ListTile(
                      leading:
                          Icon(Icons.info_outline, color: Color(0xFF7D260F)),
                      title: Text('À propos'),
                    ),
                  ),
                  const PopupMenuItem(
                    value: 'terms',
                    child: ListTile(
                      leading: Icon(Icons.rule, color: Color(0xFF7D260F)),
                      title: Text('Conditions générales'),
                    ),
                  ),
                ],
              ),
            ],
          ),
        )
      ],
    );
  }

  void _launchURL(String url) async {
    final Uri uri = Uri.parse(url);
    if (await canLaunchUrl(uri)) {
      await launchUrl(uri, mode: LaunchMode.externalApplication);
    } else {
      throw 'Impossible d\'ouvrir $url';
    }
  }

  Widget _buildBottomBar() {
    return Container(
      decoration: const BoxDecoration(
        color: Colors.transparent,
        borderRadius: BorderRadius.only(
          topLeft: Radius.circular(25),
          topRight: Radius.circular(25),
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black26,
            blurRadius: 8,
            offset: Offset(0, -2),
          )
        ],
      ),
      child: ClipRRect(
        borderRadius: const BorderRadius.only(
          topLeft: Radius.circular(25),
          topRight: Radius.circular(25),
        ),
        child: BackdropFilter(
          filter: ImageFilter.blur(sigmaX: 15.0, sigmaY: 15.0),
          child: BottomNavigationBar(
            backgroundColor: const Color.fromRGBO(245, 230, 218, 0.4),
            selectedItemColor: activeColor,
            unselectedItemColor: primaryColor,
            currentIndex: _selectedIndex,
            onTap: (int index) => setState(() => _selectedIndex = index),
            items: [
              _navItem(Icons.store, "Store", 0),
              _navItem(Icons.person, "Profil", 1),
              _navItem(Icons.settings, "Paramètres", 2),
            ],
          ),
        ),
      ),
    );
  }

  BottomNavigationBarItem _navItem(IconData icon, String label, int index) {
    final bool isSelected = _selectedIndex == index;
    final Color borderColor = isSelected ? activeColor : primaryColor;

    return BottomNavigationBarItem(
      icon: Container(
        padding: const EdgeInsets.all(6),
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          border: Border.all(color: borderColor, width: 1),
        ),
        child: Icon(icon, color: borderColor),
      ),
      label: label,
    );
  }
}
