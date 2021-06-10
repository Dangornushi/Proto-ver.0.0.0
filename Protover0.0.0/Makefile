all:
	g++ -c src/comp.cpp -std=c++14
	g++ -c src/define.cpp -std=c++14
	g++ -c src/run.cpp -std=c++14
	g++ -c src/proto.cpp -std=c++14
	g++ -c src/edit.cpp -std=c++14

	g++ edit.o define.o -o bin/edit
	g++ proto.o define.o -o bin/proto
	g++ comp.o define.o -o bin/proc
	g++ run.o define.o -o bin/prun
	rm *.o
