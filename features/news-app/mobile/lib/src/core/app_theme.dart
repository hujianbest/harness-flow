import 'package:flutter/material.dart';

class AppTheme {
  // Light Theme
  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,
      colorScheme: ColorScheme.fromSeed(
        seedColor: const Color(0xFF2196F3),
        brightness: Brightness.light,
      ),
      scaffoldBackgroundColor: const Color(0xFFFAFAFA),
      cardTheme: CardTheme(
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
          side: const BorderSide(color: Color(0xFFE0E0E0)),
        ),
      ),
      appBarTheme: const AppBarTheme(
        centerTitle: true,
        elevation: 0,
        backgroundColor: Colors.transparent,
        foregroundColor: Color(0xFF212121),
      ),
      textTheme: const TextTheme(
        headlineLarge: TextStyle(
          fontSize: 32,
          fontWeight: FontWeight.bold,
          color: Color(0xFF212121),
        ),
        headlineMedium: TextStyle(
          fontSize: 24,
          fontWeight: FontWeight.w600,
          color: Color(0xFF212121),
        ),
        titleLarge: TextStyle(
          fontSize: 18,
          fontWeight: FontWeight.w600,
          color: Color(0xFF212121),
        ),
        bodyLarge: TextStyle(
          fontSize: 16,
          color: Color(0xFF424242),
        ),
        bodyMedium: TextStyle(
          fontSize: 14,
          color: Color(0xFF616161),
        ),
      ),
    );
  }

  // Dark Theme
  static ThemeData get darkTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      colorScheme: ColorScheme.fromSeed(
        seedColor: const Color(0xFF2196F3),
        brightness: Brightness.dark,
      ),
      scaffoldBackgroundColor: const Color(0xFF121212),
      cardTheme: CardTheme(
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
          side: const BorderSide(color: Color(0xFF2C2C2C)),
        ),
      ),
      appBarTheme: const AppBarTheme(
        centerTitle: true,
        elevation: 0,
        backgroundColor: Colors.transparent,
        foregroundColor: Color(0xFFE0E0E0),
      ),
      textTheme: const TextTheme(
        headlineLarge: TextStyle(
          fontSize: 32,
          fontWeight: FontWeight.bold,
          color: Color(0xFFE0E0E0),
        ),
        headlineMedium: TextStyle(
          fontSize: 24,
          fontWeight: FontWeight.w600,
          color: Color(0xFFE0E0E0),
        ),
        titleLarge: TextStyle(
          fontSize: 18,
          fontWeight: FontWeight.w600,
          color: Color(0xFFE0E0E0),
        ),
        bodyLarge: TextStyle(
          fontSize: 16,
          color: Color(0xFFB0B0B0),
        ),
        bodyMedium: TextStyle(
          fontSize: 14,
          color: Color(0xFF909090),
        ),
      ),
    );
  }

  // Common Colors
  static const Color primaryColor = Color(0xFF2196F3);
  static const Color secondaryColor = Color(0xFF03A9F4);
  static const Color successColor = Color(0xFF4CAF50);
  static const Color warningColor = Color(0xFFFF9800);
  static const Color errorColor = Color(0xFFF44336);
}
