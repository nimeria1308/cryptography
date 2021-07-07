CPPFLAGS := -O3 -std=c++11 -Wall
LDFLAGS := -O3 -std=c++11 -Wall

%: %.cpp
	@$(CXX) $(CPPFLAGS) -o $@ $^
