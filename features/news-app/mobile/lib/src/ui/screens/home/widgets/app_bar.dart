import 'package:flutter/material.dart';

class HomeAppBar extends StatelessWidget {
  const HomeAppBar({super.key});

  @override
  Widget build(BuildContext context) {
    return SliverAppBar(
      expandedHeight: 120,
      pinned: true,
      flexibleSpace: FlexibleSpaceBar(
        title: const Text('News'),
        background: Container(
          decoration: BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter,
              colors: [
                Theme.of(context).colorScheme.primaryContainer.withOpacity(0.3),
                Theme.of(context).scaffoldBackgroundColor,
              ],
            ),
          ),
        ),
      ),
      actions: [
        IconButton(
          icon: const Icon(Icons.search_outlined),
          onPressed: () {
            // TODO: Navigate to search
          },
        ),
        IconButton(
          icon: const Icon(Icons.notifications_outlined),
          onPressed: () {
            // TODO: Open notifications
          },
        ),
      ],
    );
  }
}
