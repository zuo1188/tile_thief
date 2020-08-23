#include "stdafx.h"
#include "JpegCommentDate.h"
#include <stdio.h>
#include <limits>
#undef min
#undef max

LIBGE_NAMESPACE_BEGINE
static const int kBitsPerMonth = 4;
static const int kBitsPerDay = 5;

const int JpegCommentDate::kMinimumYear = 1;
const int JpegCommentDate::kMaximumYear = 4095;
const int JpegCommentDate::kYearUnknown = 0;
const int JpegCommentDate::kMonthUnknown = 0;
const int JpegCommentDate::kDayUnknown = 0;
const JpegCommentDate::YearMonthDayKey JpegCommentDate::kAncientDate = (1 << 9) + (1 << 5) + 1;  // 0001-01-01 oldest data for published imagery.
const JpegCommentDate kOldestJpegCommentDate(JpegCommentDate::kAncientDate);
const JpegCommentDate kUnknownJpegCommentDate;

int ParseDec32Value(const std::string& string_value, unsigned int start_index,
	size_t size, int default_result) {
	std::string substring = string_value.substr(start_index, size);
	if (substring.empty()) {
	}
	char *error = NULL;
	long long value = strtoll(substring.c_str(), &error, 10);
	// Limit long values to int min/max.  Needed for lp64; no-op on 32 bits.
	if (value > std::numeric_limits<int>::max()) {
		value = std::numeric_limits<int>::max();
	}
	else if (value < std::numeric_limits<int>::min()) {
		value = std::numeric_limits<int>::min();
	}
	// Check if there was no number to convert.
	return (error == substring.c_str()) ? default_result : value;
}

bool JpegCommentDate::YearMonthDayKeyFromInts(int year, int month, int day, YearMonthDayKey *date) 
{
	if (date == nullptr)
		return false;

	// Enforce date validity.
	bool is_input_date_valid(AreYearMonthDayValid(year, month, day));
	if (!is_input_date_valid) {
		year = kYearUnknown;
		month = kMonthUnknown;
		day = kDayUnknown;
	}
	else {
		PropagateUnknowns(year, &month, &day);
	}

	// Encode date.
	YearMonthDayKey encoded_date(static_cast<YearMonthDayKey>(year));
	encoded_date <<= kBitsPerMonth;
	encoded_date |= static_cast<YearMonthDayKey>(month);
	encoded_date <<= kBitsPerDay;
	encoded_date |= static_cast<YearMonthDayKey>(day);

	*date = encoded_date;
	return is_input_date_valid;
}

void JpegCommentDate::YearMonthDayKeyAsInts(YearMonthDayKey date, int *year, int *month, int *day) 
{
	if (year == nullptr || month==nullptr || day==nullptr)
		return;

	static const YearMonthDayKey kMonthMask = (0x1 << kBitsPerMonth) - 0x1;
	static const YearMonthDayKey kDayMask = (0x1 << kBitsPerDay) - 0x1;

	// Decode date.
	*day = static_cast<int>(date & kDayMask);
	date >>= kBitsPerDay;
	*month = static_cast<int>(date & kMonthMask);
	date >>= kBitsPerMonth;
	*year = static_cast<int>(date);
}

JpegCommentDate::JpegCommentDate(const std::string &date) 
	: year_(kYearUnknown), month_(kMonthUnknown), day_(kDayUnknown), match_all_dates_(false) 
{
	// Parse input string --- if parsing fails lines above guarantee that object
	// is properly initialized (unknown year, month and day).
	if ((date.length() < 10) || (':' != date[4] && '-' != date[4]) ||
		(':' != date[7] && '-' != date[7])) {
		return;
	}
	static const int error_value(-1);
	int year(ParseDec32Value(date, 0, 4, error_value));
	int month(ParseDec32Value(date, 5, 2, error_value));
	int day(ParseDec32Value(date, 8, 2, error_value));

	// Enforce date validity.
	if (!AreYearMonthDayValid(year, month, day)) {
		return;
	}
	PropagateUnknowns(year, &month, &day);

	year_ = year;
	month_ = month;
	day_ = day;
}

void JpegCommentDate::AppendToString(std::string *buffer) const {
	char date[11];
	// If year,month,day are unknown, this prints 0000:00:00 to indicate so.
	_snprintf_s(date, sizeof(date), "%04d:%02d:%02d", year_, month_, day_);
	buffer->append(date);
}

std::string JpegCommentDate::GetHexString() const {
	YearMonthDayKey year_month_day = AsYearMonthDayKey();
	char date[8]; // 5 digits only printed for real dates, 8 to be safe.
	_snprintf_s(date, sizeof(date), "%x", year_month_day);
	return std::string(date);
}

bool JpegCommentDate::AreYearMonthDayValid(int year, int month, int day) {
	if ((kYearUnknown != year) && ((kMinimumYear > year) ||
		(kMaximumYear < year))) {
		return false;
	}
	static const int kMinimumMonth = 1;
	static const int kMaximumMonth = 12;
	if ((kMonthUnknown != month) && ((kMinimumMonth > month) ||
		(kMaximumMonth < month))) {
		return false;
	}
	static const int kMinimumDay = 1;
	static const int kMaximumDay = 31;
	if ((kDayUnknown != day) && ((kMinimumDay > day) ||
		(kMaximumDay < day))) {
		return false;
	}
	return true;
}

void JpegCommentDate::PropagateUnknowns(int year, int *month, int *day) {
	if ((kYearUnknown == year) && (kMonthUnknown != *month)) {
		*month = kMonthUnknown;
	}
	if ((kMonthUnknown == *month) && (kDayUnknown != *day)) {
		*day = kDayUnknown;
	}
}

bool JpegCommentDate::operator==(const JpegCommentDate& other) const {
	if (year_ == other.year_ && month_ == other.month_ && day_ == other.day_)
		return true;
	return false;
}

bool JpegCommentDate::operator<(const JpegCommentDate& other) const {
	if (year_ < other.year_)
		return true;
	else if (year_ > other.year_)
		return false;
	else if (month_ < other.month_)
		return true;
	else if (month_ > other.month_)
		return false;
	else if (day_ < other.day_)
		return true;
	return false;
}
LIBGE_NAMESPACE_END
