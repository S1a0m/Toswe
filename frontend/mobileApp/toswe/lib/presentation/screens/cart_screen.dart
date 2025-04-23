import 'dart:ui';
import 'package:flutter/material.dart';

class CartScreen extends StatefulWidget {
  const CartScreen({super.key});

  @override
  State<CartScreen> createState() => _CartScreenState();
}

class _CartScreenState extends State<CartScreen> {
  final List<Map<String, dynamic>> cartItems = [
    {
      'name': 'Masque Tribal',
      'image': 'assets/images/bijou.jpeg',
      'price': 25.50,
      'quantity': 1,
    },
    {
      'name': 'Tissu Africain',
      'image': 'assets/images/bijou.jpeg',
      'price': 15.99,
      'quantity': 2,
    },
  ];

  void _incrementQuantity(int index) {
    setState(() {
      cartItems[index]['quantity']++;
    });
  }

  void _decrementQuantity(int index) {
    setState(() {
      if (cartItems[index]['quantity'] > 1) {
        cartItems[index]['quantity']--;
      }
    });
  }

  void _removeItem(int index) {
    setState(() {
      cartItems.removeAt(index);
    });
  }

  double get totalPrice => cartItems.fold(
        0.0,
        (sum, item) =>
            sum + (item['price'] as double) * (item['quantity'] as int),
      );

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
          title: const Text(
            'Mon panier',
            style: TextStyle(color: Color(0xFF7D260F)),
          ),
          centerTitle: true,
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
              child: Container(color: Colors.black.withOpacity(0)),
            ),
            SafeArea(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: cartItems.isEmpty
                    ? const Center(
                        child: Text(
                          "Votre panier est vide 🧺",
                          style: TextStyle(color: Colors.white70, fontSize: 18),
                        ),
                      )
                    : ListView(
                        children: [
                          ...cartItems.asMap().entries.map((entry) {
                            final index = entry.key;
                            final item = entry.value;
                            return AnimatedSwitcher(
                              duration: const Duration(milliseconds: 400),
                              transitionBuilder: (child, animation) =>
                                  FadeTransition(
                                opacity: animation,
                                child: SlideTransition(
                                  position: Tween<Offset>(
                                    begin: const Offset(1, 0),
                                    end: Offset.zero,
                                  ).animate(animation),
                                  child: child,
                                ),
                              ),
                              child: Container(
                                key: ValueKey(
                                    item['name'] + item['quantity'].toString()),
                                margin: const EdgeInsets.only(bottom: 16),
                                decoration: BoxDecoration(
                                  color:
                                      const Color.fromRGBO(255, 255, 255, 0.3),
                                  borderRadius: BorderRadius.circular(16),
                                  border: Border.all(color: Colors.white24),
                                ),
                                child: Row(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    ClipRRect(
                                      borderRadius: BorderRadius.circular(8),
                                      child: Image.asset(
                                        item['image'],
                                        width: 99,
                                        height: 99,
                                        fit: BoxFit.cover,
                                      ),
                                    ),
                                    const SizedBox(width: 12),
                                    Expanded(
                                      child: Column(
                                        crossAxisAlignment:
                                            CrossAxisAlignment.start,
                                        children: [
                                          Text(
                                            item['name'],
                                            style: const TextStyle(
                                                color: Colors.white,
                                                fontSize: 16),
                                          ),
                                          const SizedBox(height: 4),
                                          Text(
                                            "Prix: ${item['price']} €",
                                            style: const TextStyle(
                                                color: Colors.white70),
                                          ),
                                          const SizedBox(height: 4),
                                          Row(
                                            children: [
                                              IconButton(
                                                icon: const Icon(
                                                    Icons.remove_circle_outline,
                                                    color: Colors.white),
                                                onPressed: () =>
                                                    _decrementQuantity(index),
                                              ),
                                              Text(
                                                item['quantity'].toString(),
                                                style: const TextStyle(
                                                    color: Colors.white),
                                              ),
                                              IconButton(
                                                icon: const Icon(
                                                    Icons.add_circle_outline,
                                                    color: Colors.white),
                                                onPressed: () =>
                                                    _incrementQuantity(index),
                                              ),
                                            ],
                                          ),
                                        ],
                                      ),
                                    ),
                                    IconButton(
                                      icon: const Icon(Icons.delete_outline,
                                          color: Colors.redAccent),
                                      onPressed: () => _removeItem(index),
                                    ),
                                  ],
                                ),
                              ),
                            );
                          }).toList(),
                          const SizedBox(height: 20),
                          Container(
                            padding: const EdgeInsets.all(16),
                            decoration: const BoxDecoration(
                              color: Color.fromRGBO(245, 230, 218, 0.3),
                              borderRadius: BorderRadius.vertical(
                                  top: Radius.circular(24)),
                            ),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.stretch,
                              children: [
                                Text(
                                  "Total: ${totalPrice.toStringAsFixed(2)} €",
                                  style: const TextStyle(
                                      fontSize: 20, color: Colors.white),
                                ),
                                const SizedBox(height: 10),
                                ElevatedButton(
                                  onPressed: () {
                                    // Logique de validation
                                  },
                                  style: ElevatedButton.styleFrom(
                                    padding: const EdgeInsets.symmetric(
                                        vertical: 14),
                                    backgroundColor: const Color(0xFFC0A080),
                                    shape: RoundedRectangleBorder(
                                      borderRadius: BorderRadius.circular(12),
                                    ),
                                  ),
                                  child: const Text("Commander",
                                      style: TextStyle(fontSize: 16)),
                                )
                              ],
                            ),
                          ),
                        ],
                      ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
