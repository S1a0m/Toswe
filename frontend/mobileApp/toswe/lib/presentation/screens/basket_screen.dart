import 'package:flutter/material.dart';

class BasketScreen extends StatefulWidget {
  const BasketScreen({super.key});

  @override
  State<BasketScreen> createState() => _BasketScreenState();
}

class _BasketScreenState extends State<BasketScreen> {
  List<Map<String, dynamic>> basket = [
    {"name": "Produit A", "price": 10.0, "quantity": 2},
    {"name": "Produit B", "price": 7.5, "quantity": 3},
  ];

  void removeItem(int index) {
    setState(() => basket.removeAt(index));
  }

  double get total => basket.fold(0, (sum, item) => sum + item['price'] * item['quantity']);

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
          title: const Text("Panier", style: TextStyle(color: Color(0xFF7D260F))),
        ),
        body: Column(
          children: [
            Expanded(
              child: ListView.builder(
                itemCount: basket.length,
                itemBuilder: (context, index) {
                  final item = basket[index];
                  final totalItem = item['price'] * item['quantity'];
                  return ListTile(
                    title: Text(item['name']),
                    subtitle: Text("PU: ${item['price']} x ${item['quantity']} = ${totalItem.toStringAsFixed(2)}"),
                    trailing: IconButton(
                      icon: const Icon(Icons.delete, color: Colors.red),
                      onPressed: () => removeItem(index),
                    ),
                  );
                },
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(12.0),
              child: Column(
                children: [
                  Text("Total: ${total.toStringAsFixed(2)}", style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 10),
                  ElevatedButton(
                    onPressed: () {},
                    child: const Text("Soumettre"),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
