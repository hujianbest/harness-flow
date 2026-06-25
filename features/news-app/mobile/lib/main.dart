import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:flutter/services.dart';

import 'src/core/app_theme.dart';
import 'src/core/routes.dart';
import 'src/data/providers/auth_provider.dart';
import 'src/data/providers/article_provider.dart';
import 'src/ui/screens/home/home_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();

  // Set preferred orientations
  SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
    DeviceOrientation.portraitDown,
  ]);

  runApp(const NewsApp());
}

class NewsApp extends StatelessWidget {
  const NewsApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AuthProvider()),
        ChangeNotifierProvider(create: (_) => ArticleProvider()),
      ],
      child: MaterialApp(
        title: 'News App',
        debugShowCheckedModeBanner: false,
        theme: AppTheme.lightTheme,
        darkTheme: AppTheme.darkTheme,
        themeMode: ThemeMode.system,
        home: const HomeScreen(),
        onGenerateRoute: AppRoutes.onGenerateRoute,
      ),
    );
  }
}
