import 'dart:ui';
import 'package:flutter/material.dart';

class CartScreen extends StatefulWidget {
  const CartScreen({super.key});

  @override
  State<CartScreen> createState() => _CartScreenState();
}

class _CartScreenState extends State<CartScreen>
    with SingleTickerProviderStateMixin {
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
            4, // sum + (item['price'] as int) * item['quantity'] as int,
      );

  @override
  Widget build(BuildContext context) {
    return Stack(
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
          filter: ImageFilter.blur(sigmaX: 6, sigmaY: 6),
          child: Container(
            color: Colors.black.withOpacity(0),
          ),
        ),
        Scaffold(
          backgroundColor: Colors.transparent,
          appBar: AppBar(
            title: const Text("Mon Panier",
                style: TextStyle(color: Color(0xFF7D260F))),
            backgroundColor: const Color.fromRGBO(245, 230, 218, 0.4),
            elevation: 0,
            centerTitle: true,
          ),
          body: cartItems.isEmpty
              ? const Center(
                  child: Text(
                    "Votre panier est vide 🧺",
                    style: TextStyle(color: Colors.white70, fontSize: 18),
                  ),
                )
              : Column(
                  children: [
                    Expanded(
                      child: ListView.builder(
                        padding: const EdgeInsets.all(16),
                        itemCount: cartItems.length,
                        itemBuilder: (context, index) {
                          final item = cartItems[index];
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
                                color: const Color.fromRGBO(255, 255, 255, 0.3),
                                borderRadius: BorderRadius.circular(16),
                                border: Border.all(color: Colors.white24),
                              ),
                              child: ListTile(
                                leading: ClipRRect(
                                  borderRadius: BorderRadius.circular(8),
                                  child: Image.asset(item['image'],
                                      width: 50, height: 50, fit: BoxFit.cover),
                                ),
                                title: Text(
                                  item['name'],
                                  style: const TextStyle(color: Colors.white),
                                ),
                                subtitle: Text(
                                  "Prix: ${item['price']} €",
                                  style: const TextStyle(color: Colors.white70),
                                ),
                                trailing: Column(
                                  mainAxisAlignment: MainAxisAlignment.center,
                                  children: [
                                    Row(
                                      mainAxisSize: MainAxisSize.min,
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
                                    IconButton(
                                      icon: const Icon(Icons.delete_outline,
                                          color: Colors.redAccent),
                                      onPressed: () => _removeItem(index),
                                    )
                                  ],
                                ),
                              ),
                            ),
                          );
                        },
                      ),
                    ),
                    Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 24, vertical: 16),
                      decoration: const BoxDecoration(
                        color: Color.fromRGBO(245, 230, 218, 0.3),
                        borderRadius:
                            BorderRadius.vertical(top: Radius.circular(24)),
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
                              padding: const EdgeInsets.symmetric(vertical: 14),
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
                    )
                  ],
                ),
        )
      ],
    );
  }
}
