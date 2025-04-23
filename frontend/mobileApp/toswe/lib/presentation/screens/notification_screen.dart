import 'dart:ui';
import 'package:flutter/material.dart';

class NotificationScreen extends StatefulWidget {
  const NotificationScreen({super.key});

  @override
  State<NotificationScreen> createState() => _NotificationScreenState();
}

class _NotificationScreenState extends State<NotificationScreen> {
  List<Map<String, String>> notifications = [
    {
      "title": "Nouveau message",
      "subtitle": "Vous avez reçu un message de Khalil.",
      "icon": "message"
    },
    {
      "title": "Mise à jour disponible",
      "subtitle": "Une nouvelle version est disponible.",
      "icon": "update"
    },
    {
      "title": "Connexion sécurisée",
      "subtitle": "Vous vous êtes connecté depuis un nouvel appareil.",
      "icon": "security"
    },
  ];

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
          title:
              Text('Notification', style: TextStyle(color: Color(0xFF7D260F))),
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
              child: Padding(
                padding: const EdgeInsets.all(20),
                child: notifications.isEmpty
                    ? const Center(
                        child: Text(
                          "notification",
                          style: TextStyle(color: Colors.white70),
                        ),
                      )
                    : ListView.builder(
                        padding: const EdgeInsets.all(16),
                        itemCount: notifications.length,
                        itemBuilder: (context, index) {
                          final notif = notifications[index];
                          return Dismissible(
                            key: Key(notif["title"]! + index.toString()),
                            direction: DismissDirection.endToStart,
                            background: Container(
                              padding: const EdgeInsets.only(right: 20),
                              alignment: Alignment.centerRight,
                              color: Colors.redAccent.withOpacity(0.5),
                              child:
                                  const Icon(Icons.delete, color: Colors.white),
                            ),
                            onDismissed: (direction) {
                              setState(() {
                                notifications.removeAt(index);
                              });

                              ScaffoldMessenger.of(context).showSnackBar(
                                SnackBar(
                                  content: Text("${notif['title']} supprimée"),
                                ),
                              );
                            },
                            child: GestureDetector(
                              onTap: () => _showDetailsDialog(notif),
                              child: _buildNotificationCard(
                                title: notif["title"]!,
                                subtitle: notif["subtitle"]!,
                                icon: _getIconFromName(notif["icon"]!),
                              ),
                            ),
                          );
                        },
                      ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _showDetailsDialog(Map<String, String> notif) {
    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        backgroundColor: const Color.fromRGBO(255, 255, 255, 0.9),
        title: Text(notif["title"]!),
        content: Text(notif["subtitle"]!),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text("Fermer"),
          ),
        ],
      ),
    );
  }

  Widget _buildNotificationCard({
    required String title,
    required String subtitle,
    required IconData icon,
  }) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 10),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(14),
        child: BackdropFilter(
          filter: ImageFilter.blur(sigmaX: 4, sigmaY: 4),
          child: Container(
            decoration: BoxDecoration(
              color: const Color.fromRGBO(255, 255, 255, 0.25),
              borderRadius: BorderRadius.circular(14),
              border: Border.all(color: Colors.white.withOpacity(0.2)),
            ),
            padding: const EdgeInsets.all(16),
            child: Row(
              children: [
                Icon(icon, color: const Color(0xFFC0A080), size: 28),
                const SizedBox(width: 16),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        title,
                        style: const TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                          fontSize: 16,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        subtitle,
                        style: const TextStyle(
                          color: Colors.white70,
                          fontSize: 14,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  IconData _getIconFromName(String name) {
    switch (name) {
      case "message":
        return Icons.message_rounded;
      case "update":
        return Icons.system_update_alt_rounded;
      case "security":
        return Icons.security_rounded;
      default:
        return Icons.notifications;
    }
  }
}
