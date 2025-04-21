class Product {
  final String name;
  final String category;
  final int price;
  final List<String> images;
  final List<String> description;
  final List<Product> related;

  Product({
    required this.name,
    required this.category,
    required this.price,
    required this.images,
    required this.description,
    required this.related,
  });

  // Pour le convertir facilement depuis Map<String, dynamic> si besoin
  factory Product.fromMap(Map<String, dynamic> data) {
    return Product(
      name: data['name'],
      category: data['category'],
      price: data['price'],
      images: List<String>.from(data['images']),
      description: List<String>.from(data['description']),
      related: (data['related'] as List).map((item) => Product.fromMap(item)).toList(),
    );
  }
}
