#include "Basic.h" 
#include "MapUnit.h"
#include <vector>
#include <map>
#include <string>
#include <fstream>  // 必须包含
#include <sstream>  // 必须包含

// ... (IsBoxOverLap 和 IsRoomOverLap 函数保持不变) ...
bool IsBoxOverLap(Box box, Box other)
{
    if (other.low_left.x > box.upper_right.x ||
        other.upper_right.x < box.low_left.x ||
        other.low_left.y > box.upper_right.y ||
        other.upper_right.y < box.low_left.y) return false;
    else return true;
}

bool IsRoomOverLap(MapUnitData* room, MapUnitData* other)
{
    if (IsBoxOverLap(room->obstacle, other->obstacle)) return true;
    return false;
}

// ... (ChangePosition 保持不变) ...
void MapUnitData::ChangePosition()
{
    obstacle.low_left += velocity;
    obstacle.upper_right += velocity;
    center += velocity;
    velocity = Vec2::ZERO;
}

static MapDataManager* _instance = nullptr;

MapDataManager* MapDataManager::getInstance()
{
    if (!_instance) _instance = new MapDataManager();
    return _instance;
}

void MapDataManager::destroyInstance()
{
    if (_instance)
    {
        delete _instance;
        _instance = nullptr;
    }
}

// ---------------------------------------------------------
// 新的解析逻辑 (替代原来的 parseData 和 loadMapData)
// ---------------------------------------------------------

void MapDataManager::loadMapData(const std::string& txtFile)
{
    // 使用标准文件流读取
    std::ifstream infile(txtFile);
    if (!infile.is_open()) {
        return;
    }

    std::string line;
    std::string currentRoomName = "";
    RoomData currentRoomData;
    bool isParsingRoom = false;

    while (std::getline(infile, line))
    {
        if (line.empty()) continue;

        std::stringstream ss(line);
        std::string key;
        ss >> key; // 读取第一个单词作为关键字

        if (key == "ROOM")
        {
            // 如果之前正在解析一个房间，先保存它
            if (isParsingRoom && !currentRoomName.empty()) {
                _mapCache[currentRoomName] = currentRoomData;
            }

            // 开始新房间
            ss >> currentRoomName;
            currentRoomData = RoomData(); // 重置数据
            isParsingRoom = true;
        }
        else if (key == "SIZE")
        {
            // 格式: SIZE 宽 高
            ss >> currentRoomData.width >> currentRoomData.height;
        }
        else if (key == "ENTRANCE")
        {
            // 格式: ENTRANCE x y
            float x, y;
            ss >> x >> y;
            currentRoomData.entrances.push_back(Vec2(x, y));
        }
        else if (key == "EXIT")
        {
            // 格式: EXIT x y
            float x, y;
            ss >> x >> y;
            currentRoomData.exits.push_back(Vec2(x, y));
        }
        // 可以根据需要添加更多关键字
    }

    // 循环结束后，保存最后一个房间的数据
    if (isParsingRoom && !currentRoomName.empty()) {
        _mapCache[currentRoomName] = currentRoomData;
    }

    infile.close();
}

const RoomData* MapDataManager::getRoomData(const std::string& filename)
{
    auto it = _mapCache.find(filename);
    if (it != _mapCache.end()) return &it->second;

    // 为了防止崩溃，如果找不到数据，返回一个默认的空数据或者报错
    static RoomData emptyData;
    return &emptyData;
}