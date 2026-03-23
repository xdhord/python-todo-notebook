import json
import os
from datetime import datetime
from enum import Enum

NOTES_FILE = "notes.json"

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class TodoNoteBook:
    def __init__(self, filename=NOTES_FILE):
        self.filename = filename
        self.notes = self._load_notes()
    
    def _load_notes(self):
        """加载所有笔记"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_notes(self):
        """保存笔记到文件"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.notes, f, ensure_ascii=False, indent=2)
    
    def add_note(self, title, content, priority="MEDIUM", category="默认"):
        """添加新笔记"""
        note_id = max([n.get("id", 0) for n in self.notes] or [0]) + 1
        note = {
            "id": note_id,
            "title": title,
            "content": content,
            "priority": priority,
            "category": category,
            "completed": False,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self.notes.append(note)
        self._save_notes()
        return note
    
    def list_notes(self, category=None, completed=None):
        """列出笔记"""
        notes = self.notes
        
        if category:
            notes = [n for n in notes if n.get("category") == category]
        
        if completed is not None:
            notes = [n for n in notes if n.get("completed") == completed]
        
        return sorted(notes, key=lambda x: x["id"])
    
    def get_note(self, note_id):
        """获取单个笔记"""
        for note in self.notes:
            if note["id"] == note_id:
                return note
        return None
    
    def update_note(self, note_id, title=None, content=None, priority=None, category=None):
        """更新笔记"""
        note = self.get_note(note_id)
        if not note:
            return False
        
        if title:
            note["title"] = title
        if content:
            note["content"] = content
        if priority:
            note["priority"] = priority
        if category:
            note["category"] = category
        
        note["updated_at"] = datetime.now().isoformat()
        self._save_notes()
        return True
    
    def toggle_note(self, note_id):
        """切换笔记的完成状态"""
        note = self.get_note(note_id)
        if not note:
            return False
        
        note["completed"] = not note["completed"]
        note["updated_at"] = datetime.now().isoformat()
        self._save_notes()
        return True
    
    def delete_note(self, note_id):
        """删除笔记"""
        self.notes = [n for n in self.notes if n["id"] != note_id]
        self._save_notes()
        return True
    
    def get_stats(self):
        """获取统计信息"""
        total = len(self.notes)
        completed = sum(1 for n in self.notes if n.get("completed"))
        pending = total - completed
        categories = len(set(n.get("category", "默认") for n in self.notes))
        
        return {
            "总笔记数": total,
            "已完成": completed,
            "待办": pending,
            "分类数": categories
        }

def display_note(note):
    """格式化显示单个笔记"""
    status = "✅" if note["completed"] else "⭕"
    priority_emoji = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴"}
    emoji = priority_emoji.get(note["priority"], "🟡")
    
    print(f"\n{status} [{note['id']}] {emoji} {note['title']}")
    print(f"   分类: {note.get('category', '默认')} | 优先级: {note['priority']}")
    print(f"   内容: {note['content']}")
    print(f"   创建: {note['created_at'][:10]}")

def print_header(title):
    """打印标题"""
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")

def main():
    """主程序"""
    notebook = TodoNoteBook()
    
    while True:
        print("\n" + "🗒️  TODO 记事本".center(50))
        print("-" * 50)
        print("1️⃣  添加笔记")
        print("2️⃣  查看所有笔记")
        print("3️⃣  查看待办事项")
        print("4️⃣  查看已完成事项")
        print("5️⃣  标记完成/未完成")
        print("6️⃣  编辑笔记")
        print("7️⃣  删除笔记")
        print("8️⃣  按分类查看")
        print("9️⃣  查看统计")
        print("🔟 退出")
        print("-" * 50)
        
        choice = input("请选择操作 (1-10): ").strip()
        
        try:
            if choice == '1':
                print_header("添加新笔记")
                title = input("📝 标题: ").strip()
                if not title:
                    print("❌ 标题不能为空")
                    continue
                
                content = input("📄 内容: ").strip()
                if not content:
                    print("❌ 内容不能为空")
                    continue
                
                print("\n优先级: LOW(低) MEDIUM(中) HIGH(高)")
                priority = input("优先级 (默认MEDIUM): ").strip().upper() or "MEDIUM"
                if priority not in ["LOW", "MEDIUM", "HIGH"]:
                    priority = "MEDIUM"
                
                category = input("分类 (默认'默认'): ").strip() or "默认"
                
                note = notebook.add_note(title, content, priority, category)
                print(f"✅ 笔记已添加 (ID: {note['id']})")
            
            elif choice == '2':
                print_header("所有笔记")
                notes = notebook.list_notes()
                if notes:
                    for note in notes:
                        display_note(note)
                else:
                    print("📭 暂无笔记")
            
            elif choice == '3':
                print_header("待办事项")
                notes = notebook.list_notes(completed=False)
                if notes:
                    for note in notes:
                        display_note(note)
                else:
                    print("✨ 没有待办事项，棒棒哒！")
            
            elif choice == '4':
                print_header("已完成事项")
                notes = notebook.list_notes(completed=True)
                if notes:
                    for note in notes:
                        display_note(note)
                else:
                    print("📭 没有已完成的事项")
            
            elif choice == '5':
                print_header("标记完成/未完成")
                notes = notebook.list_notes()
                if not notes:
                    print("📭 暂无笔记")
                    continue
                
                for note in notes:
                    status = "✅" if note["completed"] else "⭕"
                    print(f"{status} [{note['id']}] {note['title']}")
                
                note_id = int(input("\n请输入笔记ID: ").strip())
                if notebook.toggle_note(note_id):
                    status = "已标记为完成" if notebook.get_note(note_id)["completed"] else "已标记为未完成"
                    print(f"✅ {status}")
                else:
                    print("❌ 笔记不存在")
            
            elif choice == '6':
                print_header("编辑笔记")
                note_id = int(input("请输入笔记ID: ").strip())
                note = notebook.get_note(note_id)
                if not note:
                    print("❌ 笔记不存在")
                    continue
                
                display_note(note)
                print("\n(按Enter保持原值)")
                
                title = input("新标题: ").strip()
                content = input("新内容: ").strip()
                priority = input("新优先级: ").strip().upper() or None
                category = input("新分类: ").strip() or None
                
                if notebook.update_note(note_id, title or None, content or None, priority, category):
                    print("✅ 笔记已更新")
                else:
                    print("❌ 更新失败")
            
            elif choice == '7':
                print_header("删除笔记")
                note_id = int(input("请输入笔记ID: ").strip())
                note = notebook.get_note(note_id)
                if not note:
                    print("❌ 笔记不存在")
                    continue
                
                print(f"确定要删除吗? \"{note['title']}\"")
                confirm = input("输入 YES 确认删除: ").strip().upper()
                if confirm == "YES":
                    notebook.delete_note(note_id)
                    print("✅ 笔记已删除")
                else:
                    print("❌ 已取消")
            
            elif choice == '8':
                print_header("按分类查看")
                categories = set(n.get("category", "默认") for n in notebook.notes)
                if not categories:
                    print("📭 暂无分类")
                    continue
                
                print("可用分类:")
                for i, cat in enumerate(categories, 1):
                    count = sum(1 for n in notebook.notes if n.get("category") == cat)
                    print(f"  {i}. {cat} ({count})")
                
                category = input("输入分类名: ").strip()
                notes = notebook.list_notes(category=category)
                if notes:
                    print(f"\n📁 分类: {category}")
                    for note in notes:
                        display_note(note)
                else:
                    print(f"📭 分类 '{category}' 中没有笔记")
            
            elif choice == '9':
                print_header("统计信息")
                stats = notebook.get_stats()
                print(f"📊 总笔记数: {stats['总笔记数']}")
                print(f"✅ 已完成: {stats['已完成']}")
                print(f"⭕ 待办: {stats['待办']}")
                print(f"📂 分类数: {stats['分类数']}")
                
                if stats['总笔记数'] > 0:
                    completion_rate = (stats['已完成'] / stats['总笔记数']) * 100
                    print(f"🎯 完成率: {completion_rate:.1f}%")
            
            elif choice == '10':
                print("\n👋 再见！")
                break
            
            else:
                print("❌ 请输入有效的选项 (1-10)")
        
        except ValueError:
            print("❌ 输入错误，请重试")
        except Exception as e:
            print(f"❌ 发生错误: {e}")

if __name__ == "__main__":
    main()
