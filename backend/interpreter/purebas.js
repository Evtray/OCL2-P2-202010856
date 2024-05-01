var index = 0;
while (index <= 200) {
    if (index == 0) {
        index = index + 5;
    } else if (index > 50) {
        index = index * 2;
    } else {
        index = (index * 2) + 1;
    }
    console.log(index);
}
