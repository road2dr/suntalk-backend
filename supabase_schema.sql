-- Supabase SQL 마이그레이션
-- suntalk_backend 데이터베이스 스키마

-- 사용자 테이블
CREATE TABLE IF NOT EXISTS public.users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL,
    nickname TEXT,
    email TEXT,
    gender TEXT CHECK (gender IN ('male', 'female', 'other')),
    age INTEGER,
    region_addr TEXT,
    kakao_id TEXT,
    naver_id TEXT,
    google_id TEXT,
    apple_id TEXT,
    thumbnail_url TEXT,
    background_image_url TEXT,
    points BIGINT DEFAULT 0,
    is_blocked BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 결제 정보 테이블
CREATE TABLE IF NOT EXISTS public.payments (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    amount INTEGER NOT NULL,
    points_earned INTEGER DEFAULT 0,
    payment_method TEXT NOT NULL CHECK (payment_method IN ('card', 'kakao_pay', 'naver_pay', 'apple_pay', 'google_pay', 'bank_transfer', 'other')),
    purpose TEXT NOT NULL CHECK (purpose IN ('subscription', 'item_purchase', 'gift', 'donation', 'coin_purchase', 'other')),
    description TEXT,
    status TEXT DEFAULT 'completed' CHECK (status IN ('pending', 'completed', 'failed', 'refunded')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 인덱스
CREATE INDEX IF NOT EXISTS idx_users_name ON public.users(name);
CREATE INDEX IF NOT EXISTS idx_users_email ON public.users(email);
CREATE INDEX IF NOT EXISTS idx_users_kakao_id ON public.users(kakao_id);
CREATE INDEX IF NOT EXISTS idx_users_naver_id ON public.users(naver_id);
CREATE INDEX IF NOT EXISTS idx_users_google_id ON public.users(google_id);
CREATE INDEX IF NOT EXISTS idx_users_apple_id ON public.users(apple_id);
CREATE INDEX IF NOT EXISTS idx_users_is_blocked ON public.users(is_blocked);
CREATE INDEX IF NOT EXISTS idx_payments_user_id ON public.payments(user_id);
CREATE INDEX IF NOT EXISTS idx_payments_created_at ON public.payments(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_payments_payment_method ON public.payments(payment_method);
CREATE INDEX IF NOT EXISTS idx_payments_purpose ON public.payments(purpose);

-- updated_at 자동 갱신 트리거
CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON public.users
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER update_payments_updated_at
    BEFORE UPDATE ON public.payments
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();

-- RLS (Row Level Security) 설정
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.payments ENABLE ROW LEVEL SECURITY;

-- 서비스 롤 전체 접근 권한
CREATE POLICY "Service role full access on users" ON public.users
    FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Service role full access on payments" ON public.payments
    FOR ALL USING (auth.role() = 'service_role');