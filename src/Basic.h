#pragma once
#include <cmath>
#include <string>
#include <vector>
#include <random>
#include <iostream>
#include <fstream>
#include <sstream>
#include <cfloat>
#include <climits>
#include <cstdarg>
#include <algorithm>

// Vec2 (¶þÎ¬ÏòÁ¿)
struct Vec2 {
    float x;
    float y;

    static const Vec2 ZERO;

    Vec2() : x(0), y(0) {}
    Vec2(float _x, float _y) : x(_x), y(_y) {}

    Vec2 operator+(const Vec2& v) const { return Vec2(x + v.x, y + v.y); }
    Vec2 operator-(const Vec2& v) const { return Vec2(x - v.x, y - v.y); }
    Vec2 operator*(float s) const { return Vec2(x * s, y * s); }
    Vec2& operator+=(const Vec2& v) { x += v.x; y += v.y; return *this; }
    Vec2& operator-=(const Vec2& v) { x -= v.x; y -= v.y; return *this; }
    Vec2& operator*=(float s) { x *= s; y *= s; return *this; }
    Vec2& operator/(float s) { x /= s; y /= s; return *this; }
    bool operator==(const Vec2& v) const { return x == v.x && y == v.y; }
    bool operator!=(const Vec2& v) const { return x != v.x || y != v.y; }

    float length() const { return std::sqrt(x * x + y * y); }

    float distance(const Vec2& v) const {
        float dx = x - v.x;
        float dy = y - v.y;
        return std::sqrt(dx * dx + dy * dy);
    }

    void normalize() {
        float l = length();
        if (l > 0) {
            x /= l;
            y /= l;
        }
    }

    static bool isLineIntersect(const Vec2& A, const Vec2& B, const Vec2& C, const Vec2& D, float* S, float* T) {
        float denom = (B.x - A.x) * (D.y - C.y) - (B.y - A.y) * (D.x - C.x);
        if (denom == 0) return false;

        float numerS = (A.y - C.y) * (D.x - C.x) - (A.x - C.x) * (D.y - C.y);
        float numerT = (A.y - C.y) * (B.x - A.x) - (A.x - C.x) * (B.y - A.y);

        *S = numerS / denom;
        *T = numerT / denom;
        return true;
    }
};

class Random {
public:
    static int random_int(int min, int max) {
        static std::random_device rd;
        static std::mt19937 gen(rd());
        std::uniform_int_distribution<> dis(min, max);
        return dis(gen);
    }
};

class FileUtils {
public:

    static FileUtils* getInstance() {
        static FileUtils instance;
        return &instance;
    }

    std::string getStringFromFile(const std::string& filename) {
        std::ifstream t(filename);
        if (!t.is_open()) {
            return "";
        }
        std::stringstream buffer;
        buffer << t.rdbuf();
        return buffer.str();
    }
};