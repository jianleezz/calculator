import streamlit as st
import random
import time

class ShootingGame:
    def __init__(self):
        self.enemies = []
        self.score = 0
        self.health = 100
        self.game_over = False
        self.game_time = 0
        
    def start_game(self):
        """게임 초기화"""
        self.enemies = [{"x": random.randint(0, 100), "y": random.randint(0, 50)} 
                       for _ in range(3)]
        self.score = 0
        self.health = 100
        self.game_over = False
        self.game_time = 0
    
    def spawn_enemy(self):
        """새로운 적 생성"""
        if random.random() < 0.3 and len(self.enemies) < 8:
            self.enemies.append({
                "x": random.randint(0, 100),
                "y": random.randint(0, 50)
            })
    
    def move_enemies(self):
        """적들의 위치 이동"""
        for enemy in self.enemies:
            enemy["y"] += random.randint(2, 5)
            if enemy["y"] > 100:
                self.health -= 10
                self.enemies.remove(enemy)
        
        if self.health <= 0:
            self.game_over = True
    
    def shoot_enemy(self, target_index):
        """적을 맞추기"""
        if 0 <= target_index < len(self.enemies):
            self.enemies.pop(target_index)
            self.score += 10
            return True
        return False

def play_shooting_game():
    """슈팅 게임 인터페이스"""
    st.subheader("🎮 간단한 슈팅 게임")
    st.write("적들을 클릭해서 없애세요! 적이 화면 아래로 떨어지면 체력이 감소합니다.")
    
    # 게임 상태 초기화
    if "game" not in st.session_state:
        st.session_state.game = ShootingGame()
        st.session_state.game.start_game()
        st.session_state.game_started = False
    
    game = st.session_state.game
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("점수", game.score, delta=0)
    with col2:
        st.metric("체력", f"{game.health}%")
    with col3:
        st.metric("남은 적", len(game.enemies))
    
    st.markdown("---")
    
    # 게임 시작 버튼
    if not st.session_state.game_started:
        if st.button("🚀 게임 시작", key="start_game"):
            st.session_state.game_started = True
            st.rerun()
    else:
        # 게임 진행 중
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # 게임 영역 표시
            game_display = "🎯 게임 영역\n"
            game_display += "=" * 50 + "\n"
            
            if len(game.enemies) == 0:
                game.spawn_enemy()
                game.spawn_enemy()
            
            # 적 위치 표시
            for i, enemy in enumerate(game.enemies):
                spaces = " " * (enemy["x"] // 2)
                game_display += f"{spaces}👾 [{i}]\n"
            
            game_display += "=" * 50
            st.code(game_display, language="text")
        
        with col1:
            st.write("**적을 선택해서 사격하세요:**")
            
            if len(game.enemies) > 0:
                col_buttons = st.columns(min(4, len(game.enemies)))
                for i, enemy in enumerate(game.enemies):
                    with col_buttons[i % 4]:
                        if st.button(f"발사 [{i}]", key=f"shoot_{i}"):
                            if game.shoot_enemy(i):
                                st.success(f"✨ 적 #{i}를 격파했습니다! +10점")
                            st.rerun()
            
            # 게임 진행
            game.move_enemies()
            time.sleep(0.5)
            
            if game.game_over:
                st.error("💥 게임 오버! 체력이 다 떨어졌습니다.")
                st.balloons()
                st.warning(f"**최종 점수: {game.score}점**")
                
                if st.button("🔄 다시 시작", key="restart_game"):
                    st.session_state.game = ShootingGame()
                    st.session_state.game.start_game()
                    st.session_state.game_started = False
                    st.rerun()
            else:
                if st.button("게임 종료", key="end_game"):
                    st.info(f"게임 종료! 최종 점수: {game.score}점")
                    st.session_state.game_started = False
                    st.rerun()
