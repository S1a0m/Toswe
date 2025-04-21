import 'package:flutter/material.dart';

class ProductDetailScreen extends StatefulWidget {
  const ProductDetailScreen({super.key});

  @override
  State<ProductDetailScreen> createState() => _ProductDetailScreenState();
}

class _ProductDetailScreenState extends State<ProductDetailScreen> {
  int _currentImage = 0;

  // Valeurs directement codées
  final Map<String, dynamic> product = {
    'name': 'Collier perlé ivoire',
    'category': 'Bijoux faits main',
    'price': 4500,
    'images': [
      'assets/images/bijou.jpeg',
      'assets/images/bijou.jpeg',
    ],
    'description': [
      'Fait à la main avec des perles naturelles.',
      'Design élégant et épuré.',
      'Parfait pour les occasions spéciales.',
    ],
    'related': [
      {
        'name': 'Bracelet cuir tressé',
        'price': 3000,
        'image': 'assets/images/bijou.jpeg',
        'description': [
          'Cuir véritable',
          'Style classique',
          'Fermeture métallique'
        ],
        'category': 'Bijoux',
        'images': ['assets/images/bijou.jpeg'],
        'related': []
      },
      {
        'name': 'Boucles d\'oreilles dorées',
        'price': 2500,
        'image': 'assets/images/bijou.jpeg',
        'description': ['Légères', 'Finition brillante', 'Anti-allergique'],
        'category': 'Bijoux',
        'images': ['assets/images/bijou.jpeg'],
        'related': []
      },
      {
        'name': 'Boucles d\'oreilles dorées',
        'price': 2500,
        'image': 'assets/images/bijou.jpeg',
        'description': ['Légères', 'Finition brillante', 'Anti-allergique'],
        'category': 'Bijoux',
        'images': ['assets/images/bijou.jpeg'],
        'related': []
      },
    ]
  };

  @override
  Widget build(BuildContext context) {
    final List<String> images = product['images'];
    final List<Map<String, dynamic>> relatedProducts =
        List<Map<String, dynamic>>.from(product['related']);

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
          title: const Text("Détails du produit",
              style: TextStyle(color: Color(0xFF7D260F))),
          backgroundColor: const Color.fromRGBO(245, 230, 218, 0.5),
          foregroundColor: Colors.white,
        ),
        body: ListView(
          children: [
            // Carousel
            SizedBox(
              height: 250,
              child: PageView.builder(
                itemCount: images.length,
                onPageChanged: (index) {
                  setState(() {
                    _currentImage = index;
                  });
                },
                itemBuilder: (context, index) {
                  return Image.asset(
                    images[index],
                    fit: BoxFit.cover,
                  );
                },
              ),
            ),
            // Dots
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: List.generate(images.length, (index) {
                return AnimatedContainer(
                  duration: const Duration(milliseconds: 300),
                  margin:
                      const EdgeInsets.symmetric(horizontal: 4, vertical: 8),
                  width: _currentImage == index ? 12 : 8,
                  height: 8,
                  decoration: BoxDecoration(
                    color: _currentImage == index
                        ? const Color(0xFF7D260F)
                        : Colors.grey,
                    borderRadius: BorderRadius.circular(4),
                  ),
                );
              }),
            ),
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    product['name'],
                    style: const TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                      fontFamily: 'Playfair Display',
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    product['category'],
                    style: const TextStyle(
                      color: Colors.grey,
                      fontSize: 14,
                    ),
                  ),
                  const SizedBox(height: 10),
                  Text(
                    "${product['price']} fcfa",
                    style: const TextStyle(
                      fontSize: 18,
                      color: Color(0xFF7D260F),
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 10),
                  ElevatedButton.icon(
                    onPressed: () {
                      // Ajouter au panier
                    },
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFF7D260F),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                      padding: const EdgeInsets.symmetric(
                          horizontal: 16, vertical: 12),
                    ),
                    icon: const Icon(Icons.add_shopping_cart,
                        color: Color(0xFFF5E6DA)),
                    label: const Text(
                      "Ajouter au panier",
                      style: TextStyle(color: Color(0xFFF5E6DA)),
                    ),
                  ),
                  const SizedBox(height: 16),
                  const Text(
                    "Description",
                    style: TextStyle(
                      fontWeight: FontWeight.w600,
                      fontSize: 18,
                      fontFamily: 'Playfair Display',
                    ),
                  ),
                  const SizedBox(height: 8),
                  ...List.generate(product['description'].length, (i) {
                    return Padding(
                      padding: const EdgeInsets.only(bottom: 4),
                      child: Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text("• ", style: TextStyle(fontSize: 16)),
                          Expanded(
                            child: Text(
                              product['description'][i],
                              style: const TextStyle(fontSize: 16),
                            ),
                          ),
                        ],
                      ),
                    );
                  }),
                  const SizedBox(height: 24),
                  const Text(
                    "Produits similaires",
                    style: TextStyle(
                      fontWeight: FontWeight.w600,
                      fontSize: 18,
                      fontFamily: 'Playfair Display',
                    ),
                  ),
                  const SizedBox(height: 12),
                  SizedBox(
                    height: 180,
                    child: ListView.builder(
                      scrollDirection: Axis.horizontal,
                      itemCount: relatedProducts.length,
                      itemBuilder: (context, index) {
                        final related = relatedProducts[index];
                        return Container(
                          width: 140,
                          margin: const EdgeInsets.only(right: 12),
                          decoration: BoxDecoration(
                            color: const Color(0xFFF5E6DA),
                            borderRadius: BorderRadius.circular(16),
                            boxShadow: const [
                              BoxShadow(
                                color: Colors.black12,
                                blurRadius: 4,
                                offset: Offset(2, 2),
                              ),
                            ],
                          ),
                          child: Column(
                            children: [
                              Expanded(
                                child: ClipRRect(
                                  borderRadius: const BorderRadius.vertical(
                                      top: Radius.circular(16)),
                                  child: Image.asset(
                                    related['image'],
                                    width: double.infinity,
                                    fit: BoxFit.cover,
                                  ),
                                ),
                              ),
                              Padding(
                                padding: const EdgeInsets.all(8),
                                child: Column(
                                  children: [
                                    Text(
                                      related['name'],
                                      maxLines: 1,
                                      overflow: TextOverflow.ellipsis,
                                      style: const TextStyle(
                                          fontWeight: FontWeight.w600),
                                    ),
                                    Text(
                                      "${related['price']} fcfa",
                                      style: const TextStyle(
                                          color: Color(0xFF7D260F)),
                                    ),
                                    TextButton(
                                      onPressed: () {
                                        Navigator.push(
                                          context,
                                          MaterialPageRoute(
                                            builder: (_) =>
                                                ProductDetailScreen(),
                                          ),
                                        );
                                      },
                                      child: const Text("Voir"),
                                    ),
                                  ],
                                ),
                              )
                            ],
                          ),
                        );
                      },
                    ),
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
