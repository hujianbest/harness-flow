import 'package:flutter/foundation.dart';

enum AuthStatus { unknown, authenticated, unauthenticated }

class AuthProvider with ChangeNotifier {
  AuthStatus _status = AuthStatus.unknown;
  String? _token;
  String? _userId;

  AuthStatus get status => _status;
  String? get token => _token;
  String? get userId => _userId;
  bool get isAuthenticated => _status == AuthStatus.authenticated;

  // Mock user data (replace with API calls)
  Future<void> checkAuthStatus() async {
    // In production, check local storage or validate token
    _status = AuthStatus.unauthenticated;
    notifyListeners();
  }

  Future<bool> login({
    required String email,
    required String password,
  }) async {
    try {
      // TODO: Call API login endpoint
      // For now, simulate successful login
      await Future.delayed(const Duration(milliseconds: 500));

      _token = 'mock-jwt-token';
      _userId = 'mock-user-id';
      _status = AuthStatus.authenticated;
      notifyListeners();
      return true;
    } catch (e) {
      _status = AuthStatus.unauthenticated;
      notifyListeners();
      return false;
    }
  }

  Future<bool> register({
    required String email,
    required String password,
    required String name,
  }) async {
    try {
      // TODO: Call API register endpoint
      await Future.delayed(const Duration(milliseconds: 500));

      _token = 'mock-jwt-token';
      _userId = 'mock-user-id';
      _status = AuthStatus.authenticated;
      notifyListeners();
      return true;
    } catch (e) {
      return false;
    }
  }

  Future<void> logout() async {
    _token = null;
    _userId = null;
    _status = AuthStatus.unauthenticated;
    notifyListeners();
  }
}
