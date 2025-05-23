// 인증 관련 API 서비스

// 백엔드 API 기본 URL
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

/**
 * 회원가입 함수
 * @param {Object} userData 사용자 정보 객체
 * @returns {Promise} API 응답 Promise
 */
export const signup = async (userData) => {
  try {
    // 실제 API 연결 - 현재는 주석 처리
    // const response = await fetch(`${API_URL}/signup/`, {
    //   method: 'POST',
    //   headers: {
    //     'Content-Type': 'application/json',
    //   },
    //   body: JSON.stringify(userData)
    // });
    
    // if (!response.ok) {
    //   const errorData = await response.json();
    //   throw new Error(errorData.message || '회원가입 처리 중 오류가 발생했습니다.');
    // }
    // return await response.json();
    
    // 임시 로컬 스토리지 구현
    const existingUsers = JSON.parse(localStorage.getItem('registeredUsers') || '[]');
    
    // 아이디 중복 검사
    if (existingUsers.some(user => user.username === userData.username)) {
      throw new Error('이미 사용 중인 아이디입니다.');
    }
    
    // 새 사용자 추가
    existingUsers.push({...userData});
    
    // 저장
    localStorage.setItem('registeredUsers', JSON.stringify(existingUsers));
    
    return { 
      success: true, 
      message: '회원가입이 완료되었습니다.' 
    };
    
  } catch (error) {
    console.error('회원가입 오류:', error);
    throw error;
  }
};

/**
 * 로그인 함수
 * @param {string} username 사용자 아이디
 * @param {string} password 비밀번호
 * @returns {Promise} API 응답 Promise
 */
export const login = async (username, password) => {
  try {
    // 현재 상태에서 백엔드 서버 연결 여부 확인
    let isBackendConnected = false;
    
    try {
      // 백엔드 연결 상태 확인 (5초 타임아웃)
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 3000);
      
      const checkResponse = await fetch(`${API_URL}/accounts/login/`, {
        method: 'HEAD',
        signal: controller.signal
      }).catch(() => null);
      
      clearTimeout(timeoutId);
      
      isBackendConnected = checkResponse && checkResponse.ok;
      console.log('백엔드 연결 상태:', isBackendConnected ? '연결됨' : '연결 안됨');
    } catch (checkError) {
      console.log('백엔드 연결 확인 실패:', checkError);
      isBackendConnected = false;
    }
    
    // 백엔드가 연결된 경우 실제 API 호출
    if (isBackendConnected) {
      console.log('백엔드 서버로 로그인 요청 전송');
      
      const response = await fetch(`${API_URL}/accounts/login/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password })
      });
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || '로그인 처리 중 오류가 발생했습니다.');
      }
      
      const data = await response.json();
      localStorage.setItem('token', data.token || 'backend-token');
      localStorage.setItem('user', JSON.stringify(data.user || { username }));
      return data;
    } else {
      console.log('백엔드 연결 불가, 로컬 스토리지 로그인 사용');
      
      // 임시 로컬 스토리지 구현
      const registeredUsers = JSON.parse(localStorage.getItem('registeredUsers') || '[]');
      console.log('등록된 사용자 수:', registeredUsers.length);
      
      const user = registeredUsers.find(u => u.username === username && u.password === password);
      
      if (!user) {
        throw new Error('아이디 또는 비밀번호가 일치하지 않습니다.');
      }
      
      // 비밀번호를 제외한 사용자 정보 저장
      const { password: _, ...userInfo } = user;
      localStorage.setItem('user', JSON.stringify(userInfo));
      localStorage.setItem('token', 'demo-token-' + Math.random().toString(36).substr(2));
      
      return { 
        success: true, 
        user: userInfo, 
        token: localStorage.getItem('token'),
        message: '로그인이 완료되었습니다.' 
      };
    }
    
  } catch (error) {
    console.error('로그인 오류:', error);
    throw error;
  }
};

/**
 * 로그아웃 함수
 */
export const logout = () => {
  // 실제 API 연결 - 현재는 주석 처리
  // return fetch(`${API_URL}/logout/`, {
  //   method: 'POST',
  //   headers: {
  //     'Authorization': `Bearer ${localStorage.getItem('token')}`
  //   }
  // }).finally(() => {
  //   localStorage.removeItem('token');
  //   localStorage.removeItem('user');
  // });
  
  // 임시 로컬 스토리지 구현
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  
  return Promise.resolve({ success: true, message: '로그아웃이 완료되었습니다.' });
};

/**
 * 사용자 프로필 정보를 가져오는 함수
 * @returns {Promise} 사용자 정보 Promise
 */
export const getUserProfile = async () => {
  try {
    // 실제 API 연결 - 현재는 주석 처리
    // const response = await fetch(`${API_URL}/profile/`, {
    //   headers: {
    //     'Authorization': `Bearer ${localStorage.getItem('token')}`
    //   }
    // });
    
    // if (!response.ok) {
    //   if (response.status === 401) {
    //     // 인증 실패 시 로그아웃 처리
    //     logout();
    //     throw new Error('인증이 만료되었습니다. 다시 로그인해주세요.');
    //   }
    //   throw new Error('프로필 정보를 가져오는 중 오류가 발생했습니다.');
    // }
    
    // return await response.json();
    
    // 임시 로컬 스토리지 구현
    const userData = localStorage.getItem('user');
    const hasToken = localStorage.getItem('token');
    
    console.log('사용자 데이터 확인:', !!userData);
    console.log('토큰 확인:', !!hasToken);
    
    if (!userData) {
      throw new Error('로그인 정보가 없습니다. 다시 로그인해주세요.');
    }
    
    // 토큰이 없는 경우
    if (!hasToken) {
      localStorage.removeItem('user'); // 일관성을 위해 사용자 정보도 제거
      throw new Error('로그인이 만료되었습니다. 다시 로그인해주세요.');
    }
    
    try {
      const parsedUserData = JSON.parse(userData);
      
      // 기본 필드 검증
      if (!parsedUserData.username) {
        throw new Error('사용자 정보가 올바르지 않습니다.');
      }
      
      return parsedUserData;
    } catch (parseError) {
      console.error('사용자 데이터 파싱 오류:', parseError);
      localStorage.removeItem('user');
      throw new Error('사용자 정보가 손상되었습니다. 다시 로그인해주세요.');
    }
    
  } catch (error) {
    console.error('프로필 정보 가져오기 오류:', error);
    throw error;
  }
};

/**
 * 사용자 프로필 정보 업데이트 함수
 * @param {Object} userData 업데이트할 사용자 정보
 * @returns {Promise} 업데이트된 사용자 정보 Promise
 */
export const updateUserProfile = async (userData) => {
  try {
    // 실제 API 연결 - 현재는 주석 처리
    // const response = await fetch(`${API_URL}/profile/update/`, {
    //   method: 'PUT',
    //   headers: {
    //     'Content-Type': 'application/json',
    //     'Authorization': `Bearer ${localStorage.getItem('token')}`
    //   },
    //   body: JSON.stringify(userData)
    // });
    
    // if (!response.ok) {
    //   if (response.status === 401) {
    //     logout();
    //     throw new Error('인증이 만료되었습니다. 다시 로그인해주세요.');
    //   }
    //   throw new Error('프로필 정보 업데이트 중 오류가 발생했습니다.');
    // }
    
    // const updatedUser = await response.json();
    // localStorage.setItem('user', JSON.stringify(updatedUser));
    // return updatedUser;
    
    // 임시 로컬 스토리지 구현
    const currentUser = JSON.parse(localStorage.getItem('user'));
    
    if (!currentUser) {
      throw new Error('로그인 정보가 없습니다. 다시 로그인해주세요.');
    }
    
    // 현재 사용자 ID 확인
    const username = currentUser.username;
    
    // 등록된 사용자 목록 불러오기
    const registeredUsers = JSON.parse(localStorage.getItem('registeredUsers') || '[]');
    
    // 사용자 찾기
    const userIndex = registeredUsers.findIndex(user => user.username === username);
    
    if (userIndex === -1) {
      throw new Error('사용자 정보를 찾을 수 없습니다.');
    }
    
    // 사용자 정보 업데이트 (비밀번호는 보존)
    const password = registeredUsers[userIndex].password;
    registeredUsers[userIndex] = { ...userData, username, password };
    
    // 변경된 정보 저장
    localStorage.setItem('registeredUsers', JSON.stringify(registeredUsers));
    
    // 현재 사용자 정보도 업데이트
    const { password: _, ...updatedUserInfo } = registeredUsers[userIndex];
    localStorage.setItem('user', JSON.stringify(updatedUserInfo));
    
    return updatedUserInfo;
    
  } catch (error) {
    console.error('프로필 정보 업데이트 오류:', error);
    throw error;
  }
};

/**
 * 사용자 로그인 상태 확인 함수
 * @returns {boolean} 로그인 상태
 */
export const isAuthenticated = () => {
  const hasToken = localStorage.getItem('token') !== null;
  const hasUser = localStorage.getItem('user') !== null;
  
  if (hasToken !== hasUser) {
    // 불일치하는 상태 처리 (토큰만 있거나 사용자 정보만 있는 경우)
    console.warn('인증 상태 불일치: 토큰과 사용자 정보가 일치하지 않습니다.');
    
    // 불일치 상태 정리
    if (!hasToken || !hasUser) {
      logout();
      return false;
    }
  }
  
  return hasToken && hasUser;
};
