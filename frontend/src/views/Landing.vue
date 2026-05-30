<template>
  <div class="landing">
    <nav class="landing-nav">
      <span class="brand">Veerabhadra Matrimony</span>
      <div class="nav-links">
        <RouterLink to="/login" class="btn btn-secondary" style="padding: 8px 20px; font-size: 14px;">Sign In</RouterLink>
        <RouterLink to="/register" class="btn btn-primary" style="padding: 8px 20px; font-size: 14px;">Register Free</RouterLink>
      </div>
    </nav>

    <section class="hero">
      <div class="hero-inner">
        <h1 class="hero-title">Find Your Perfect Match</h1>
        <p class="hero-sub">Trusted by thousands of families across India. Start your journey to a meaningful relationship today.</p>
        <div class="hero-actions">
          <RouterLink to="/register" class="btn btn-primary" style="padding: 14px 36px; font-size: 16px;">Create Free Profile</RouterLink>
          <RouterLink to="/login" class="btn btn-secondary" style="padding: 14px 36px; font-size: 16px;">Already registered? Sign In</RouterLink>
        </div>
      </div>
    </section>

    <section class="features">
      <div class="feature-card">
        <div class="feature-icon">🔍</div>
        <h3>Smart Matching</h3>
        <p>Advanced filters for religion, caste, education, and location to find exactly who you're looking for.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">💬</div>
        <h3>Direct Chat</h3>
        <p>Connect and chat privately once both sides show interest. Safe, verified, and secure.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">✅</div>
        <h3>Verified Profiles</h3>
        <p>Government ID verification and photo moderation ensure only genuine profiles.</p>
      </div>
    </section>

    <footer class="landing-footer">
      <p>© 2026 Veerabhadra Matrimony. All rights reserved.</p>
    </footer>
  </div>
</template>

<style scoped>
.landing {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f7f2f2;
}

.landing-nav {
  background: #fff;
  border-bottom: 1px solid #eee;
  padding: 0 32px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 10;
}

.brand {
  font-size: 18px;
  font-weight: 800;
  color: #c0392b;
  letter-spacing: -0.3px;
}

.nav-links {
  display: flex;
  gap: 10px;
  align-items: center;
}

.hero {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 80px 24px;
  background: linear-gradient(135deg, #fff5f5 0%, #fff 60%, #f7f2f2 100%);
}

.hero-inner {
  text-align: center;
  max-width: 600px;
}

.hero-title {
  font-size: 48px;
  font-weight: 800;
  color: #1a1a1a;
  line-height: 1.15;
  margin-bottom: 16px;
}

.hero-sub {
  font-size: 18px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 36px;
}

.hero-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}

.features {
  display: flex;
  gap: 20px;
  justify-content: center;
  padding: 48px 24px;
  flex-wrap: wrap;
  background: #fff;
  border-top: 1px solid #eee;
}

.feature-card {
  background: #fafafa;
  border: 1px solid #eee;
  border-radius: 12px;
  padding: 28px 24px;
  max-width: 260px;
  text-align: center;
  flex: 1;
  min-width: 200px;
}

.feature-icon {
  font-size: 32px;
  margin-bottom: 12px;
}

.feature-card h3 {
  font-size: 16px;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 8px;
}

.feature-card p {
  font-size: 14px;
  color: #888;
  line-height: 1.6;
}

.landing-footer {
  background: #1a1a1a;
  color: #888;
  text-align: center;
  padding: 20px;
  font-size: 13px;
}
</style>
