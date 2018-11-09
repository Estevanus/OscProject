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
extern "C" OSCLIB_API double *kali4(double a, double b);
extern "C" OSCLIB_API double kali5(double a, double b);
extern "C" OSCLIB_API int loopAll(int max);
extern "C" OSCLIB_API PyObject kali3(float a, PyObject b);


// ----------------------------- My Lib Data -----------------------------
extern "C" OSCLIB_API double getMaxSpeed(double force, double airDensity, double drag, double frontalArea);
// -----------------------------------------------------------------------


