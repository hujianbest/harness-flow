import 'package:flutter/foundation.dart';

class Article {
  final String id;
  final String title;
  final String? summary;
  final String? sourceName;
  final String? sourceIcon;
  final DateTime? publishedAt;
  final List<String> tags;
  final int readTime;
  final int? qualityScore;

  Article({
    required this.id,
    required this.title,
    this.summary,
    this.sourceName,
    this.sourceIcon,
    this.publishedAt,
    this.tags = const [],
    this.readTime = 0,
    this.qualityScore,
  });

  factory Article.fromJson(Map<String, dynamic> json) {
    final source = json['source'] as Map<String, dynamic>?;
    return Article(
      id: json['id'] as String,
      title: json['title'] as String,
      summary: json['summary'] as String?,
      sourceName: source?['name'] as String?,
      sourceIcon: source?['icon'] as String?,
      publishedAt: json['publishedAt'] != null
          ? DateTime.parse(json['publishedAt'] as String)
          : null,
      tags: (json['tags'] as List?)?.cast<String>() ?? [],
      readTime: json['readTime'] as int? ?? 0,
      qualityScore: json['qualityScore'] as int?,
    );
  }
}

class ArticleProvider with ChangeNotifier {
  List<Article> _articles = [];
  bool _isLoading = false;
  String? _error;

  List<Article> get articles => _articles;
  bool get isLoading => _isLoading;
  String? get error => _error;

  Future<void> loadArticles({
    int page = 1,
    int pageSize = 20,
  }) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      // TODO: Call API articles endpoint
      // For now, simulate API call
      await Future.delayed(const Duration(milliseconds: 800));

      // Mock data
      _articles = [
        Article(
          id: '1',
          title: 'AI 技术突破：新模型实现更高效推理',
          summary: '研究人员开发出新的神经网络架构，显著提升推理效率...',
          sourceName: 'TechNews',
          sourceIcon: 'https://example.com/tech.png',
          publishedAt: DateTime.now().subtract(const Duration(hours: 2)),
          tags: ['AI', '科技', '创新'],
          readTime: 5,
          qualityScore: 4,
        ),
        Article(
          id: '2',
          title: '全球市场动态：科技股领涨',
          summary: '受AI热潮推动，科技股今日大幅上涨...',
          sourceName: 'BusinessDaily',
          publishedAt: DateTime.now().subtract(const Duration(hours: 4)),
          tags: ['财经', '市场'],
          readTime: 3,
          qualityScore: 3,
        ),
      ];

      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> refresh() async {
    await loadArticles();
  }
}
