# Baby Android 2
Description:
```markdown
If you've never reverse engineered an Android application, now is the time!! Get to it, already!! Learn more about how they work!!

[baby-android-2.apk]
```

**Author**: `overllama`

## Writeup
TL;DR this time, the functions actually matter, since it checks your flag. You can run the app and see the input being checked yourself, though I probably should have made it display as you typed lol. Then the input is processed and you get a good message if you get it right. The catch is the code is introduced through a native library. Luckily, that C++ code is pretty simple.

Open the apk in jadx and you'll see the MainActivity that program does an `onClick()` function that gathers your input from a field and then runs it through `FlagChecker.check()`.

```java
public void onClick(View view) {
    String flagAttempt = MainActivity.this.flag.getText().toString();
    TextView banner = (TextView) MainActivity.this.findViewById(R.id.banner);
    if (FlagChecker.check(flagAttempt)) {
        banner.setText("That's the right flag!!!");
    } else {
        banner.setText("Nope! Try again if you'd like");
    }
}
```

However, looking at the FlagChecker function, it just looks like this:
```java
public class FlagChecker {
    public static native boolean check(String str);

    static {
        System.loadLibrary("babyandroid");
    }
}
```

All it does is load in the `babyandroid` library. What does that mean? That's a Native Library, which uses the JNI to load compiled C/C++ code into the Java code running in the App in the Android. So the `System.loadLibrary` function loads in a native lib. And the `public static native` definition just says "this is defined in native code."

If you jump back into jadx and go to **Resources > lib > whatever_arch** it'll store the library `.so` files for all native libraries. I'll pull the arm library, just for funsies. You can do this by right clicking on the file and clicking `Export`.

Opening the file in a decompiler, we find this function:
```c++
uint64_t Java_byuctf_babyandroid_FlagChecker_check(_jstring* arg1, int64_t arg2, uint8_t* arg3)
    void* fsbase
    int64_t rax = *(fsbase + 0x28)
    int64_t var_40 = arg2
    _JNIEnv::GetStringUTFChars(arg1, arg3)
    char var_28[0x18]
    std::__ndk1::basic_strin...char> >::basic_string<std::nullptr_t>(&var_28)
    char var_29
    
    if (sub_4206f0(&var_28) == 0x17)
        int32_t var_58_1 = 0
        
        while (true)
            if (var_58_1 s>= 0x17)
                var_29 = 1
                int32_t var_54_2 = 1
                break
            
            if (sx.d(*sub_420710(&var_28, sx.q(var_58_1))) != sx.d((
                    *"bycnu)_aacGly~}tt+?=<_ML?f^i_vET…")[sx.q(mods.dp.d(sx.q(var_58_1 * var_58_1), 
                    0x2f))]))
                var_29 = 0
                int32_t var_54_1 = 1
                break
            
            var_58_1 += 1
    else
        var_29 = 0
        int32_t var_54 = 1
    
    std::__ndk1::basic_strin...dk1::allocator<char> >::~basic_string()
    
    if (*(fsbase + 0x28) == rax)
        int64_t rax_12
        rax_12.b = var_29
        return zx.q(rax_12.b)
    
    __stack_chk_fail()
    noreturn
```

It takes a `_jstring` pointer, which is how the JNI can pass String objects to C/C++. In this case, I wrote the code and therefore know that it was C++. This gets parsed into a `char[]` object in memory as `var_28`, which is then used in a flag check. It looks like this is checking if `var_28[i] == stored[i*i % 0x2f]`, so we can reproduce that in python and profit:

```python
>>> info = "bycnu)_aacGly~}tt+?=<_ML?f^i_vETkG+b{nDJrVp6=)="
>>> for i in range(0x2f):
...     print(info[(i*i)%0x2f], end='')
...     
byuctf{c++_in_an_apk??}yy}??kpa_na_ni_++c{ftcuy
```

There's the flag!

**Flag** - `byuctf{c++_in_an_apk??}`