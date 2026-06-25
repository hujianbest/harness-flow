import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';

import '../../../../data/providers/article_provider.dart';

class ArticleCard extends StatelessWidget {
  final Article article;

  const ArticleCard({super.key, required this.article});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: InkWell(
        borderRadius: BorderRadius.circular(12),
        onTap: () {
          // TODO: Navigate to article detail
        },
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Header: Source and Quality
              Row(
                children: [
                  if (article.sourceIcon != null)
                    ClipRRect(
                      borderRadius: BorderRadius.circular(4),
                      child: CachedNetworkImage(
                        imageUrl: article.sourceIcon!,
                        width: 20,
                        height: 20,
                        placeholder: (_, __) => const SizedBox(width: 20, height: 20),
                        errorWidget: (_, __, ___) => const Icon(Icons.public, size: 20),
                      ),
                    ),
                  if (article.sourceName != null) ...[
                    const SizedBox(width: 8),
                    Text(
                      article.sourceName!,
                      style: theme.textTheme.bodySmall,
                    ),
                  ],
                  const Spacer(),
                  if (article.qualityScore != null)
                    _buildQualityStars(article.qualityScore!),
                ],
              ),
              const SizedBox(height: 12),

              // Title
              Text(
                article.title,
                style: theme.textTheme.titleLarge,
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
              const SizedBox(height: 8),

              // Summary
              if (article.summary != null)
                Text(
                  article.summary!,
                  style: theme.textTheme.bodyMedium,
                  maxLines: 3,
                  overflow: TextOverflow.ellipsis,
                ),
              const SizedBox(height: 12),

              // Footer: Tags, Read Time, Published
              Wrap(
                spacing: 8,
                children: [
                  // Tags
                  if (article.tags.isNotEmpty)
                    ...article.tags.take(2).map(
                      (tag) => Chip(
                        label: Text(tag),
                        visualDensity: VisualDensity.compact,
                        padding: EdgeInsets.zero,
                        materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
                      ),
                    ),

                  // Read time
                  if (article.readTime > 0)
                    Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        const Icon(Icons.schedule, size: 14),
                        const SizedBox(width: 4),
                        Text('${article.readTime} min'),
                      ],
                    ),

                  // Published time
                  if (article.publishedAt != null)
                    Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        const Icon(Icons.access_time, size: 14),
                        const SizedBox(width: 4),
                        Text(_formatTime(article.publishedAt!)),
                      ],
                    ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildQualityStars(int score) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: List.generate(
        5,
        (index) => Icon(
          index < score ? Icons.star : Icons.star_border,
          size: 14,
          color: Colors.amber,
        ),
      ),
    );
  }

  String _formatTime(DateTime dateTime) {
    final now = DateTime.now();
    final difference = now.difference(dateTime);

    if (difference.inMinutes < 60) {
      return '${difference.inMinutes}m ago';
    } else if (difference.inHours < 24) {
      return '${difference.inHours}h ago';
    } else {
      return '${difference.inDays}d ago';
    }
  }
}
