@__const.main.key = private unnamed_addr constant [50 x i32] [i32 119, i32 20, i32 96, i32 6, i32 50, i32 80, i32 43, i32 28, i32 117, i32 22, i32 125, i32 34, i32 21, i32 116, i32 23, i32 124, i32 35, i32 18, i32 35, i32 85, i32 56, i32 103, i32 14, i32 96, i32 20, i32 39, i32 85, i32 56, i32 93, i32 57, i32 8, i32 60, i32 72, i32 45, i32 114, i32 0, i32 101, i32 21, i32 103, i32 84, i32 39, i32 66, i32 44, i32 27, i32 122, i32 77, i32 36, i32 20, i32 122, i32 7], align 16
@.str = private unnamed_addr constant [14 x i8] c"Input FLAG : \00", align 1
@.str.1 = private unnamed_addr constant [3 x i8] c"%s\00", align 1
@.str.2 = private unnamed_addr constant [22 x i8] c"Correct! FLAG is %s.\0A\00", align 1
@.str.3 = private unnamed_addr constant [16 x i8] c"Incorrect FLAG.\00", align 1

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca [70 x i8], align 16
  %3 = alloca [50 x i32], align 16
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  %6 = alloca i64, align 8
  store i32 0, i32* %1, align 4
  %7 = bitcast [50 x i32]* %3 to i8*
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 16 %7, i8* align 16 bitcast ([50 x i32]* @__const.main.key to i8*), i64 200, i1 false)
  %8 = call i32 (i8*, ...) @printf(i8* noundef getelementptr inbounds ([14 x i8], [14 x i8]* @.str, i64 0, i64 0))
  %9 = getelementptr inbounds [70 x i8], [70 x i8]* %2, i64 0, i64 0
  %10 = call i32 (i8*, ...) @__isoc99_scanf(i8* noundef getelementptr inbounds ([3 x i8], [3 x i8]* @.str.1, i64 0, i64 0), i8* noundef %9)
  %11 = getelementptr inbounds [70 x i8], [70 x i8]* %2, i64 0, i64 0
  %12 = call i64 @strlen(i8* noundef %11) #4
  %13 = icmp eq i64 %12, 49
  br i1 %13, label %14, label %48

14:                                               ; preds = %0
  store i32 0, i32* %4, align 4
  store i32 0, i32* %5, align 4
  store i64 0, i64* %6, align 8
  br label %15

15:                                               ; preds = %38, %14
  %16 = load i64, i64* %6, align 8
  %17 = icmp ult i64 %16, 49
  br i1 %17, label %18, label %41

18:                                               ; preds = %15
  %19 = load i64, i64* %6, align 8
  %20 = getelementptr inbounds [70 x i8], [70 x i8]* %2, i64 0, i64 %19
  %21 = load i8, i8* %20, align 1
  %22 = sext i8 %21 to i32
  %23 = load i64, i64* %6, align 8
  %24 = getelementptr inbounds [50 x i32], [50 x i32]* %3, i64 0, i64 %23
  %25 = load i32, i32* %24, align 4
  %26 = xor i32 %22, %25
  %27 = load i64, i64* %6, align 8
  %28 = add i64 %27, 1
  %29 = getelementptr inbounds [50 x i32], [50 x i32]* %3, i64 0, i64 %28
  %30 = load i32, i32* %29, align 4
  %31 = xor i32 %26, %30
  store i32 %31, i32* %5, align 4
  %32 = load i32, i32* %5, align 4
  %33 = icmp eq i32 %32, 0
  br i1 %33, label %34, label %37

34:                                               ; preds = %18
  %35 = load i32, i32* %4, align 4
  %36 = add nsw i32 %35, 1
  store i32 %36, i32* %4, align 4
  br label %37

37:                                               ; preds = %34, %18
  br label %38

38:                                               ; preds = %37
  %39 = load i64, i64* %6, align 8
  %40 = add i64 %39, 1
  store i64 %40, i64* %6, align 8
  br label %15, !llvm.loop !6

41:                                               ; preds = %15
  %42 = load i32, i32* %4, align 4
  %43 = icmp eq i32 %42, 49
  br i1 %43, label %44, label %47

44:                                               ; preds = %41
  %45 = getelementptr inbounds [70 x i8], [70 x i8]* %2, i64 0, i64 0
  %46 = call i32 (i8*, ...) @printf(i8* noundef getelementptr inbounds ([22 x i8], [22 x i8]* @.str.2, i64 0, i64 0), i8* noundef %45)
  store i32 0, i32* %1, align 4
  br label %50

47:                                               ; preds = %41
  br label %48

48:                                               ; preds = %47, %0
  %49 = call i32 @puts(i8* noundef getelementptr inbounds ([16 x i8], [16 x i8]* @.str.3, i64 0, i64 0))
  store i32 1, i32* %1, align 4
  br label %50

50:                                               ; preds = %48, %44
  %51 = load i32, i32* %1, align 4
  ret i32 %51
}
