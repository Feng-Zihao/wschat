CXX=clang++
CXX_FLAGS=-g -MMD -fno-exceptions -std=c++11
LD_FLAGS=
INCLUDE_SEARCH_PATH=
SRCS=$(wildcard *.cpp **/*.cpp)
OBJS=$(patsubst %.cpp, obj/%.o, $(SRCS))

.PHONY: clean

main:$(OBJS)
	$(CXX) $(CXX_FLAGS) -o $@ $^
	@echo '===================='

info:
	@echo $(SRCS)
	@echo $(OBJS)


obj/%.o:%.cpp *.h
	$(CXX) $(CXX_FLAGS) -c -o $@ $<

clean:
	@rm obj/*.o -f
	@rm obj/**/*.o -f
	@rm main -f
