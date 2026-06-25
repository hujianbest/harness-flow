import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../../data/providers/article_provider.dart';
import '../../../../data/providers/auth_provider.dart';
import 'widgets/article_card.dart';
import 'widgets/app_bar.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final ScrollController _scrollController = ScrollController();

  @override
  void initState() {
    super.initState();
    _loadArticles();
  }

  Future<void> _loadArticles() async {
    final provider = context.read<ArticleProvider>();
    await provider.loadArticles();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: CustomScrollView(
        controller: _scrollController,
        slivers: [
          const HomeAppBar(),
          SliverToBoxAdapter(
            child: Consumer2<ArticleProvider, AuthProvider>(
              builder: (context, articleProvider, authProvider, child) {
                if (articleProvider.isLoading) {
                  return const Center(
                    child: Padding(
                      padding: EdgeInsets.all(32.0),
                      child: CircularProgressIndicator(),
                    ),
                  );
                }

                if (articleProvider.error != null) {
                  return Center(
                    child: Padding(
                      padding: const EdgeInsets.all(32.0),
                      child: Column(
                        children: [
                          const Icon(Icons.error_outline, size: 48),
                          const SizedBox(height: 16),
                          Text(articleProvider.error!),
                          const SizedBox(height: 16),
                          ElevatedButton(
                            onPressed: _loadArticles,
                            child: const Text('Retry'),
                          ),
                        ],
                      ),
                    ),
                  );
                }

                final articles = articleProvider.articles;
                if (articles.isEmpty) {
                  return const Center(
                    child: Padding(
                      padding: EdgeInsets.all(32.0),
                      child: Text('No articles available'),
                    ),
                  );
                }

                return Column(
                  children: articles.map((article) => ArticleCard(article: article)).toList(),
                );
              },
            ),
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }
}
