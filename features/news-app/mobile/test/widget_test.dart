import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:news_app/main.dart';
import 'package:news_app/src/data/providers/article_provider.dart';
import 'package:news_app/src/ui/screens/home/home_screen.dart';

void main() {
  group('News App Widget Tests', () {
    testWidgets('HomeScreen renders loading state', (tester) async {
      await tester.pumpWidget(
        MultiProvider(
          providers: [
            ChangeNotifierProvider(create: (_) => ArticleProvider()..loadArticles()),
          ],
          child: const MaterialApp(home: HomeScreen()),
        ),
      );

      // Initially shows loading indicator
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });

    testWidgets('ArticleCard displays article information', (tester) async {
      const article = Article(
        id: '1',
        title: 'Test Article',
        summary: 'Test summary',
        sourceName: 'Test Source',
        tags: ['Tech', 'News'],
        readTime: 5,
        qualityScore: 4,
      );

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: ArticleCard(article: article),
          ),
        ),
      );

      expect(find.text('Test Article'), findsOneWidget);
      expect(find.text('Test summary'), findsOneWidget);
      expect(find.text('Test Source'), findsOneWidget);
      expect(find.text('Tech'), findsOneWidget);
      expect(find.text('News'), findsOneWidget);
      expect(find.text('5 min'), findsOneWidget);
    });
  });
}
