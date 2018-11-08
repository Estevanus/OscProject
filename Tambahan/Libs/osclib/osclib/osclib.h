#pragma once

#include "Python.h"

#ifdef OSCLIB_EXPORTS
#define OSCLIB_API __declspec(dllexport)
#else
#define OSCLIB_API __declspec(dllexport)
#endif // OSCLIB_EXPORTS

extern "C" OSCLIB_API int kali(int a, int b);
//int kali(int a, int b);
//extern "C" OSCLIB_API double kali2(double x, double y);
extern "C" OSCLIB_API float kali2(float a, float b);
extern "C" OSCLIB_API PyObject kali3(float a, PyObject b);


