import 'package:flutter/material.dart';

class NotificationScreen extends StatefulWidget {
  const NotificationScreen({super.key});

  @override
  State<NotificationScreen> createState() => _NotificationScreenState();
}

class _NotificationScreenState extends State<NotificationScreen> {
  List<Map<String, String>> notifications = [
    {
      'title': 'Nouvelle commande',
      'content': 'Une nouvelle commande a été passée...',
      'date': '2025-04-20 13:45',
    },
    {
      'title': 'Offre spéciale',
      'content': 'Profitez de 20% de réduction...',
      'date': '2025-04-19 09:30',
    },
  ];

  void clearAll() {
    setState(() => notifications.clear());
  }

  void deleteNotification(int index) {
    setState(() => notifications.removeAt(index));
  }

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
          backgroundColor: const Color.fromRGBO(245, 230, 218, 0.5),
          title: const Text("Notifications",
              style: TextStyle(color: Color(0xFF7D260F))),
          actions: [
            IconButton(
              onPressed: clearAll,
              icon: const Icon(Icons.delete_forever, color: Color(0xFF7D260F)),
              tooltip: 'Tout effacer',
            ),
          ],
        ),
        body: ListView.builder(
          itemCount: notifications.length,
          itemBuilder: (context, index) {
            final notif = notifications[index];
            return Dismissible(
              key: Key(notif['title']! + notif['date']!),
              direction: DismissDirection.endToStart,
              onDismissed: (_) => deleteNotification(index),
              background: Container(
                color: Colors.red,
                alignment: Alignment.centerRight,
                padding: const EdgeInsets.symmetric(horizontal: 20),
                child: const Icon(Icons.delete, color: Colors.white),
              ),
              child: Card(
                margin: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                child: ListTile(
                  title: Text(notif['title']!,
                      style: const TextStyle(fontWeight: FontWeight.bold)),
                  subtitle: Text(
                    '${notif['content']!.length > 60 ? notif['content']!.substring(0, 60) + '...' : notif['content']!}\n${notif['date']}',
                    style: const TextStyle(color: Colors.grey),
                  ),
                  isThreeLine: true,
                ),
              ),
            );
          },
        ),
      ),
    );
  }
}
