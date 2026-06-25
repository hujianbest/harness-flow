import 'package:flutter/material.dart';

class AppRoutes {
  static const String home = '/';
  static const String search = '/search';
  static const String favorites = '/favorites';
  static const String profile = '/profile';
  static const String articleDetail = '/article/:id';

  static Route<dynamic> onGenerateRoute(RouteSettings settings) {
    switch (settings.name) {
      case home:
        return MaterialPageRoute(
          builder: (_) => const _PlaceholderScreen(title: 'Home'),
        );
      case search:
        return MaterialPageRoute(
          builder: (_) => const _PlaceholderScreen(title: 'Search'),
        );
      case favorites:
        return MaterialPageRoute(
          builder: (_) => const _PlaceholderScreen(title: 'Favorites'),
        );
      case profile:
        return MaterialPageRoute(
          builder: (_) => const _PlaceholderScreen(title: 'Profile'),
        );
      default:
        return MaterialPageRoute(
          builder: (_) => const _PlaceholderScreen(title: 'Not Found'),
        );
    }
  }
}

class _PlaceholderScreen extends StatelessWidget {
  final String title;

  const _PlaceholderScreen({required this.title});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(title)),
      body: Center(
        child: Text('$title Screen - Coming Soon'),
      ),
    );
  }
}
