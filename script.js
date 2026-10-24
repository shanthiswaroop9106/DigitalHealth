const legacyTranslations = {
  en: {
    brand: "HealthSync",
    navHome: "Home",
    navDashboard: "Dashboard",
    navDiet: "Diet",
    navActivities: "Activities",
    navProgress: "Progress",
    navAssistant: "AI Assistant",
    navProfile: "Profile",
    navLogin: "Login",
    navSignup: "Sign Up",
    heroTitle: "Personalized diabetes care that fits your daily life.",
    heroText: "Track meals, activity, progress, and wellness insights in one compassionate digital companion.",
    heroPrimary: "Get started",
    heroSecondary: "See dashboard",
    heroPoint1: "Daily guidance",
    heroPoint2: "Better habits",
    heroPoint3: "Smarter health",
    ctaTitle: "Ready to build healthier habits with confidence?",
    ctaButton: "Create account",
    sectionFeature: "Why people choose HealthSync",
    sectionBenefit: "Built around your health goals",
    sectionSummary: "Your health snapshots",
    loginTitle: "Welcome back",
    signupTitle: "Create your account",
    onboardingTitle: "Tell us about your health journey",
    dashboardTitle: "Health overview",
    profileTitle: "Profile & settings"
  },
  te: {
    brand: "హెల్త్సింక్",
    navHome: "హోమ్",
    navDashboard: "డాష్‌బోర్డ్",
    navDiet: "ఆహారం",
    navActivities: "చర్యలు",
    navProgress: "ప్రగ్రెస్",
    navAssistant: "AI సహాయకుడు",
    navProfile: "ప్రొఫైల్",
    navLogin: "లాగిన్",
    navSignup: "సైన్ అప్",
    heroTitle: "మీ రోజువారీ జీవితానికి అనుగుణంగా వ్యక్తిగత డయాబెటిస్ సేవ.",
    heroText: "ఆహారం, శారీరక చైతన్యం, ప్రగ్రెస్ మరియు ఆరోగ్య సూచనలు ఒకే స్మార్ట్గా ట్రాక్ చేయండి.",
    heroPrimary: "ప్రారంభించండి",
    heroSecondary: "డాష్‌బోర్డ్ చూడండి",
    heroPoint1: "రోజువారీ మార్గదర్శకం",
    heroPoint2: "మెరుగైన అలవాట్లు",
    heroPoint3: "చురుకైన ఆరోగ్యం",
    ctaTitle: "ఆరోగ్య అలవాట్లను నమ్మకంగా నిర్మించేందుకు సిద్దంగా ఉన్నారా?",
    ctaButton: "ఖాతాను సృష్టించండి",
    sectionFeature: "హెల్త్సింక్ను ఎందుకు ఎంచుకుంటారు",
    sectionBenefit: "మీ ఆరోగ్య లక్ష్యాలకు అనుగుణంగా రూపొందించబడింది",
    sectionSummary: "మీ ఆరోగ్య సంగ్రహణాలు",
    loginTitle: "మరలా స్వాగతం",
    signupTitle: "మీ ఖాతాను సృష్టించండి",
    onboardingTitle: "మీ ఆరోగ్య ప్రయాణం గురించి చెప్పండి",
    dashboardTitle: "ఆరోగ్య అవలోకనం",
    profileTitle: "ప్రొఫైల్ మరియు సెట్టింగ్స్"
  },
  hi: {
    brand: "हेल्थसिंक",
    navHome: "होम",
    navDashboard: "डैशबोर्ड",
    navDiet: "डाइट",
    navActivities: "एक्टिविटीज",
    navProgress: "प्रगति",
    navAssistant: "AI सहायक",
    navProfile: "प्रोफ़ाइल",
    navLogin: "लॉगिन",
    navSignup: "साइन अप",
    heroTitle: "आपके रोज़ाना जीवन के लिए व्यक्तिगत मधुमेह देखभाल।",
    heroText: "एक ही जगह पर भोजन, गतिविधि, प्रगति और स्वास्थ्य सुझावों को ट्रैक करें।",
    heroPrimary: "शुरू करें",
    heroSecondary: "डैशबोर्ड देखें",
    heroPoint1: "दैनिक मार्गदर्शन",
    heroPoint2: "बेहतर आदतें",
    heroPoint3: "स्मार्ट स्वास्थ्य",
    ctaTitle: "आत्मविश्वास के साथ स्वस्थ आदतें बनाने के लिए तैयार हैं?",
    ctaButton: "अकाउंट बनाएं",
    sectionFeature: "लोग हेल्थसिंक को क्यों चुनते हैं",
    sectionBenefit: "आपके स्वास्थ्य लक्ष्यों के अनुरूप बनाया गया",
    sectionSummary: "आपका स्वास्थ्य सारांश",
    loginTitle: "वापसी पर स्वागत है",
    signupTitle: "अपना अकाउंट बनाएं",
    onboardingTitle: "अपने स्वास्थ्य सफर के बारे में बताएं",
    dashboardTitle: "स्वास्थ्य अवलोकन",
    profileTitle: "प्रोफ़ाइल और सेटिंग्स"
  }
};

const translations = window.healthSyncTranslations || legacyTranslations;
let currentLanguage = 'en';
let currentUser = null;
const originalTextNodes = new WeakMap();
const originalAttributes = new WeakMap();
const originalDocumentTitle = document.title;
const originalMetaDescription = document.querySelector('meta[name="description"]')?.content || '';

function t(key, values = {}) {
  const dictionary = translations[currentLanguage] || translations.en || {};
  return String(dictionary[key] ?? translations.en?.[key] ?? key)
    .replace(/\{(\w+)\}/g, (_, name) => values[name] ?? `{${name}}`);
}

function applyLanguage(language) {
  currentLanguage = translations[language] ? language : 'en';
  const dictionary = translations[currentLanguage] || {};
  document.documentElement.lang = currentLanguage;

  document.querySelectorAll('[data-i18n]').forEach((element) => {
    const key = element.dataset.i18n;
    if (dictionary[key] || translations.en?.[key]) {
      element.textContent = t(key);
    }
  });

  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let node;
  while ((node = walker.nextNode())) {
    const parent = node.parentElement;
    if (!parent || parent.closest('[data-i18n], script, style, [data-no-translate]')) continue;
    let source = originalTextNodes.get(node);
    if (source === undefined) {
      source = node.nodeValue;
      originalTextNodes.set(node, source);
    }
    const phrase = source.trim();
    if (!phrase) continue;
    const translated = t(phrase);
    if (translated !== phrase) {
      const leading = source.match(/^\s*/)?.[0] || '';
      const trailing = source.match(/\s*$/)?.[0] || '';
      node.nodeValue = `${leading}${translated}${trailing}`;
    } else if (currentLanguage === 'en') {
      node.nodeValue = source;
    }
  }

  document.querySelectorAll('input[placeholder], textarea[placeholder], [aria-label], [title], [data-i18n-placeholder]').forEach((element) => {
    for (const attribute of ['placeholder', 'aria-label', 'title']) {
      if (!element.hasAttribute(attribute)) continue;
      let source = originalAttributes.get(element)?.[attribute];
      if (source === undefined) {
        source = element.getAttribute(attribute);
        const stored = originalAttributes.get(element) || {};
        stored[attribute] = source;
        originalAttributes.set(element, stored);
      }
      element.setAttribute(attribute, t(source));
    }
  });

  document.querySelectorAll('[data-language]').forEach((select) => {
    select.value = currentLanguage;
  });

  document.querySelectorAll('[data-question]').forEach((button) => {
    if (!button.dataset.questionSource) {
      button.dataset.questionSource = button.dataset.question;
    }
    button.dataset.question = t(button.dataset.questionSource);
  });
  if (originalDocumentTitle) document.title = t(originalDocumentTitle);
  const description = document.querySelector('meta[name="description"]');
  if (description && originalMetaDescription) description.content = t(originalMetaDescription);
  updateWelcomeName();
  window.dispatchEvent(new CustomEvent('healthsync:languagechange', { detail: currentLanguage }));
}

function setActiveNav() {
  const page = window.location.pathname.split('/').pop() || 'index.html';
  const links = document.querySelectorAll('.main-nav a, .sidebar-nav a');
  links.forEach((link) => {
    const href = link.getAttribute('href');
    if (href === page) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });
}

function setupMobileNav() {
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.querySelector('.main-nav');
  if (!toggle || !nav) return;

  toggle.addEventListener('click', () => {
    nav.style.display = nav.style.display === 'flex' ? 'none' : 'flex';
    nav.style.flexDirection = 'column';
    nav.style.position = 'absolute';
    nav.style.top = '72px';
    nav.style.left = '16px';
    nav.style.right = '16px';
    nav.style.background = '#fff';
    nav.style.padding = '18px';
    nav.style.borderRadius = '18px';
    nav.style.border = '1px solid var(--line)';
    nav.style.boxShadow = 'var(--shadow)';
  });
}

function initFormFeedback() {
  document.querySelectorAll('form:not([id])').forEach((form) => {
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      const status = form.querySelector('.form-status');
      if (status) {
        status.textContent = t('Form submitted successfully in this frontend demo.');
      }
    });
  });
}

function initSwitches() {
  document.querySelectorAll('.switch').forEach((switchEl) => {
    switchEl.addEventListener('click', async () => {
      if (!currentUser) return;
      const setting = switchEl.dataset.setting;
      if (!setting) return;
      const enabled = !switchEl.classList.contains('on');
      switchEl.disabled = true;
      try {
        const response = await fetch('/api/settings', {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ [setting]: enabled })
        });
        const result = await response.json();
        if (!response.ok || !result.success) {
          throw new Error(result.error || 'Unable to save settings.');
        }
        switchEl.classList.toggle('on', enabled);
        switchEl.setAttribute('aria-pressed', String(enabled));
      } catch (error) {
        console.error('Unable to save user setting:', error);
        const status = document.getElementById('profileStatus');
        if (status) status.textContent = t('Unable to save settings.');
      } finally {
        switchEl.disabled = false;
      }
    });
  });
}

function initLanguageSelector() {
  const selects = document.querySelectorAll('[data-language]');
  selects.forEach((select) => {
    select.addEventListener('change', (event) => {
      const language = event.target.value;
      applyLanguage(language);
      if (!currentUser) {
        localStorage.setItem('healthsync-lang', language);
        return;
      }

      fetch('/api/settings/language', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ language })
      }).then(async (response) => {
        const result = await response.json();
        if (!response.ok || !result.success) {
          throw new Error(result.error || t('Unable to save language preference.'));
        }
        const status = document.getElementById('languageStatus');
        if (status) status.textContent = t('Language preference saved.');
      }).catch((error) => {
        console.error('Unable to save language preference:', error);
        const status = document.getElementById('languageStatus');
        if (status) status.textContent = t('Unable to save language preference.');
      });
    });
  });
  applyLanguage(localStorage.getItem('healthsync-lang') || 'en');
  selects.forEach((select) => {
    select.addEventListener('change', () => {
      initDashboard();
      initProgressTracker();
    });
  });
}

function initYear() {
  const yearTarget = document.getElementById('year');
  if (yearTarget) {
    yearTarget.textContent = new Date().getFullYear();
  }
}

function updateWelcomeName() {
  if (!currentUser) return;
  const firstName = currentUser.user.firstName || currentUser.user.email;
  const fullName = [currentUser.user.firstName, currentUser.user.lastName].filter(Boolean).join(' ')
    || currentUser.user.email;
  const name = document.getElementById('dashboardUserName');
  const avatar = document.getElementById('dashboardAvatar');
  const details = document.getElementById('dashboardUserDetails');
  const welcome = document.getElementById('dashboardWelcome');
  if (name) name.textContent = fullName;
  if (avatar) {
    const initials = [currentUser.user.firstName, currentUser.user.lastName]
      .filter(Boolean)
      .map((part) => part[0])
      .join('')
      .toUpperCase();
    avatar.textContent = initials || currentUser.user.email[0].toUpperCase();
  }
  if (details) {
    details.textContent = currentUser.profile?.diabetes_category
      || t('Complete your health profile');
  }
  if (welcome) welcome.textContent = t('Hello, {name}', { name: firstName });

  const accountLink = document.getElementById('signedInAccount');
  if (accountLink) accountLink.textContent = fullName;
}

async function loadCurrentUser() {
  try {
    const response = await fetch('/api/me');
    if (response.status === 401) {
      currentUser = null;
      applyLanguage(localStorage.getItem('healthsync-lang') || 'en');
      return null;
    }
    const result = await response.json();
    if (!response.ok || !result.success) {
      throw new Error(result.error || t('Unable to load your profile. Please log in again.'));
    }

    currentUser = result;
    localStorage.removeItem('healthsync-lang');
    applyLanguage(result.user.language || 'en');
    document.querySelectorAll('[data-setting]').forEach((toggle) => {
      const setting = toggle.dataset.setting;
      const enabled = Boolean(result.settings?.[setting]);
      toggle.classList.toggle('on', enabled);
      toggle.setAttribute('aria-pressed', String(enabled));
    });
    const loginLink = document.querySelector('.nav-actions a[href="login.html"]');
    const signupLink = document.querySelector('.nav-actions a[href="signup.html"]');
    const navActions = document.querySelector('.nav-actions');
    if (loginLink) loginLink.hidden = true;
    if (signupLink) signupLink.hidden = true;
    if (navActions && !document.getElementById('signedInAccount')) {
      const accountLink = document.createElement('a');
      accountLink.id = 'signedInAccount';
      accountLink.className = 'muted-link';
      accountLink.href = 'profile.html';
      navActions.appendChild(accountLink);

      const logoutButton = document.createElement('button');
      logoutButton.id = 'logoutButton';
      logoutButton.className = 'btn btn-outline';
      logoutButton.type = 'button';
      logoutButton.textContent = t('Log out');
      logoutButton.addEventListener('click', async () => {
        logoutButton.disabled = true;
        try {
          const logoutResponse = await fetch('/api/auth/logout', { method: 'POST' });
          const logoutResult = await logoutResponse.json();
          if (!logoutResponse.ok || !logoutResult.success) {
            throw new Error(logoutResult.error || 'Unable to log out.');
          }
          currentUser = null;
          window.location.href = '/login.html';
        } catch (error) {
          console.error('Logout failed:', error);
          logoutButton.disabled = false;
        }
      });
      navActions.appendChild(logoutButton);
    } else {
      const logoutButton = document.getElementById('logoutButton');
      if (logoutButton) logoutButton.textContent = t('Log out');
    }
    updateWelcomeName();
    return result;
  } catch (error) {
    console.error('Unable to load current account:', error);
    return null;
  }
}

function populateProfileForm(form, current) {
  const profile = current.profile || {};
  const fields = {
    firstName: current.user.firstName || '',
    lastName: current.user.lastName || '',
    email: current.user.email || '',
    age: profile.age ?? '',
    gender: profile.gender || '',
    diabetesCategory: (profile.diabetes_category || '').replace(/\s+diabetes$/i, ''),
    height: profile.height_cm ?? '',
    weight: profile.weight_kg ?? '',
    activityLevel: profile.activity_level || '',
    lifestyle: profile.lifestyle || '',
    foodPreferences: profile.food_preferences || '',
    healthConditions: profile.health_conditions || '',
    goals: profile.goals || '',
    notes: profile.notes || ''
  };
  for (const [name, value] of Object.entries(fields)) {
    const field = form.elements.namedItem(name);
    if (field) field.value = value;
  }
}

function renderProfileSummary(current) {
  const summary = document.getElementById('profileSummary');
  if (!summary) return;
  const fullName = [current.user.firstName, current.user.lastName].filter(Boolean).join(' ');
  summary.textContent = [fullName, current.user.email].filter(Boolean).join(' • ');
}

async function initDashboard() {
  const category = document.getElementById('dashboardCategory');
  if (!category) return;
  if (!currentUser) return;

  const profile = currentUser.profile || {};
  const record = currentUser.latestRecord || {};
  const noData = t('Not available');
  const diabetes = profile.diabetes_category && profile.diabetes_category !== 'Not specified'
    ? t(profile.diabetes_category.replace(/\s+diabetes$/i, ''))
    : noData;
  category.textContent = diabetes;
  document.getElementById('dashboardDiabetesBadge').textContent = diabetes;
  document.getElementById('dashboardConditions').textContent =
    profile.health_conditions || t('No conditions added');

  const bmi = document.getElementById('dashboardBmi');
  const bmiBadge = document.getElementById('dashboardBmiBadge');
  bmi.textContent = profile.bmi ?? noData;
  bmiBadge.textContent = profile.bmi == null ? noData : t('BMI recorded');

  const stepsValue = document.getElementById('dashboardStepsValue');
  const stepsBadge = document.getElementById('dashboardStepsBadge');
  const stepsDelta = document.getElementById('dashboardStepsDelta');
  stepsValue.textContent = record.steps == null ? noData : Number(record.steps).toLocaleString(currentLanguage);
  stepsBadge.textContent = record.steps == null ? noData : `${(record.steps / 1000).toLocaleString(currentLanguage, { maximumFractionDigits: 1 })}k`;
  if (record.steps != null) {
    const remaining = Math.max(10000 - record.steps, 0).toLocaleString(currentLanguage);
    stepsDelta.textContent = record.steps >= 10000
      ? t('Daily step goal reached')
      : t('Need {count} more steps', { count: remaining });
  } else {
    stepsDelta.textContent = t('No step data recorded');
  }

  const glucoseSummary = document.getElementById('dashboardGlucoseSummary');
  glucoseSummary.textContent = record.blood_glucose == null
    ? t('No blood sugar reading recorded')
    : t('Blood sugar reading: {value} mg/dL', { value: record.blood_glucose });
  document.getElementById('dashboardHydrationSummary').textContent = record.hydration_liters == null
    ? t('No hydration data recorded')
    : t('Hydration recorded: {value} L', { value: record.hydration_liters });
  document.getElementById('dashboardSleepSummary').textContent = record.sleep_hours == null
    ? t('No sleep data recorded')
    : t('Sleep recorded: {value} hours', { value: record.sleep_hours });

  try {
    const date = new Date().toISOString().slice(0, 10);
    const response = await fetch(`/api/diet/status?date=${encodeURIComponent(date)}`);
    const result = await response.json();
    if (!response.ok || !result.success) throw new Error(result.error || response.statusText);
    document.getElementById('dashboardMealsBadge').textContent = `${result.completed}/${result.total}`;
    document.getElementById('dashboardMealsValue').textContent =
      result.completed === result.total ? t('All meals completed') : t('Meals completed: {count}', { count: result.completed });
    document.getElementById('dashboardMealsDelta').textContent =
      t('Diet progress: {percentage}%', { percentage: result.percentage });
  } catch (error) {
    console.error('Unable to load dashboard meal progress:', error);
  }
}

async function initProgressTracker() {
  const overall = document.getElementById('progressOverall');
  if (!overall || !currentUser) return;
  const setProgress = (name, percentage) => {
    document.getElementById(`progress${name}`).textContent = `${percentage}%`;
    document.getElementById(`progress${name}Bar`).style.width = `${percentage}%`;
  };

  try {
    const date = new Date().toISOString().slice(0, 10);
    const [dietResponse, activityResponse] = await Promise.all([
      fetch(`/api/diet/status?date=${encodeURIComponent(date)}`),
      fetch(`/api/activity/status?date=${encodeURIComponent(date)}`)
    ]);
    const [diet, activity] = await Promise.all([dietResponse.json(), activityResponse.json()]);
    if (!dietResponse.ok || !diet.success) throw new Error(diet.error || dietResponse.statusText);
    if (!activityResponse.ok || !activity.success) throw new Error(activity.error || activityResponse.statusText);

    const profile = currentUser.profile || {};
    const completionFields = [
      currentUser.user.firstName,
      currentUser.user.email,
      profile.age,
      profile.gender,
      profile.height_cm,
      profile.weight_kg,
      profile.diabetes_category,
      profile.activity_level
    ];
    const profileCompletion = Math.round(
      completionFields.filter((value) => value !== null && value !== undefined && value !== '').length
      / completionFields.length * 100
    );
    const percentages = [diet.percentage, activity.percentage, profileCompletion];
    setProgress('Diet', diet.percentage);
    setProgress('Activity', activity.percentage);
    setProgress('Profile', profileCompletion);
    const average = Math.round(percentages.reduce((sum, value) => sum + value, 0) / percentages.length);
    overall.textContent = `${average}%`;
    document.getElementById('progressOverallBar').style.width = `${average}%`;
  } catch (error) {
    console.error('Unable to load progress data:', error);
  }
}

async function initProfilePage() {
  const form = document.getElementById('profileForm');
  const editor = document.getElementById('profileEditor');
  const editButton = document.getElementById('editProfileBtn');
  const cancelButton = document.getElementById('cancelProfileEdit');
  const status = document.getElementById('profileStatus');
  if (!form || !editor || !editButton) return;

  const current = currentUser || await loadCurrentUser();
  if (!current) {
    if (status) status.textContent = t('Please log in to view your profile.');
    editButton.disabled = true;
    return;
  }
  populateProfileForm(form, current);
  renderProfileSummary(current);

  editButton.addEventListener('click', () => {
    populateProfileForm(form, currentUser);
    status.textContent = '';
    editor.hidden = false;
    document.getElementById('profile-first-name').focus();
  });
  cancelButton.addEventListener('click', () => {
    populateProfileForm(form, currentUser);
    status.textContent = '';
    editor.hidden = true;
  });
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const values = Object.fromEntries(new FormData(form).entries());
    const payload = {
      ...values,
      age: values.age || null,
      height: values.height || null,
      weight: values.weight || null
    };
    try {
      const response = await fetch('/api/profile', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const result = await response.json();
      if (!response.ok || !result.success) {
        status.textContent = t(result.error || 'Error saving profile. Please try again.');
        return;
      }
      const refreshed = await fetch('/api/me');
      const refreshedResult = await refreshed.json();
      if (!refreshed.ok || !refreshedResult.success) {
        throw new Error(refreshedResult.error || t('Error saving profile. Please try again.'));
      }
      currentUser = refreshedResult;
      populateProfileForm(form, currentUser);
      renderProfileSummary(currentUser);
      updateWelcomeName();
      status.textContent = t('Profile updated successfully.');
      editor.hidden = true;
    } catch (error) {
      console.error('Profile update failed:', error);
      status.textContent = t(error.message || 'Error saving profile. Please try again.');
    }
  });
}

function initAuthForms() {
  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const formData = new FormData(loginForm);
      const email = formData.get('email');
      const password = formData.get('password');
      const status = loginForm.querySelector('.form-status');

      try {
        const response = await fetch('/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });
        const result = await response.json();
        if (status) status.textContent = t(result.error || 'Login successful.');
        if (response.ok && result.success) {
          localStorage.removeItem('healthsync-lang');
          window.location.href = result.redirect || '/dashboard.html';
        }
      } catch (error) {
        console.error('Login request failed:', error);
        if (status) status.textContent = t('Unable to log in. Please try again.');
      }
    });
  }

  const signupForm = document.getElementById('signupForm');
  if (signupForm) {
    signupForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const formData = new FormData(signupForm);
      const payload = {
        firstName: formData.get('firstName') || '',
        lastName: formData.get('lastName') || '',
        email: formData.get('email') || '',
        password: formData.get('password') || '',
        goal: formData.get('goal') || '',
        language: currentLanguage
      };
      const status = signupForm.querySelector('.form-status');

      try {
        const response = await fetch('/api/auth/signup', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const result = await response.json();
        if (status) status.textContent = t(result.error || 'Account created successfully.');
        if (response.ok && result.success) {
          localStorage.removeItem('healthsync-lang');
          window.location.href = result.redirect || '/onboarding.html';
        }
      } catch (error) {
        console.error('Signup request failed:', error);
        if (status) status.textContent = t('Unable to create your account. Please try again.');
      }
    });
  }

  const onboardingForm = document.getElementById('onboardingForm');
  if (onboardingForm) {
    onboardingForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const formData = new FormData(onboardingForm);
      const payload = {
        age: formData.get('age') || null,
        gender: formData.get('gender') || '',
        height: formData.get('height') || null,
        weight: formData.get('weight') || null,
        diabetesCategory: formData.get('diabetesCategory') || '',
        activityLevel: formData.get('activityLevel') || '',
        healthConditions: formData.get('healthConditions') || '',
        foodPreferences: formData.get('foodPreferences') || '',
        lifestyle: formData.get('lifestyle') || '',
        goals: formData.get('goals') || '',
        notes: formData.get('notes') || ''
      };
      const status = onboardingForm.querySelector('.form-status');

      try {
        const response = await fetch('/api/onboarding', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const result = await response.json();
        if (status) status.textContent = t(result.error || 'Great — your profile is ready.');
        if (response.ok && result.success) {
          window.location.href = result.redirect || '/dashboard.html';
        }
      } catch (error) {
        console.error('Onboarding request failed:', error);
        if (status) status.textContent = t('Unable to save your health details. Please try again.');
      }
    });
  }
}

function initAiAssistant() {
  const chatBox = document.querySelector('.chat-box');
  const chatInput = document.getElementById('chatInput');
  const sendButton = document.getElementById('sendChatBtn');
  const chatStatus = document.getElementById('chatStatus');
  const quickButtons = document.querySelectorAll('.quick-button');
  const chatHistoryList = document.getElementById('chatHistoryList');
  const newChatButton = document.getElementById('newChatBtn');

  if (!chatBox || !chatInput || !sendButton) {
    return;
  }

  const addMessage = (text, sender) => {
    const message = document.createElement('div');
    message.className = `message ${sender}`;
    message.textContent = text;
    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight;
  };

  let isLoading = false;
  const setLoadingState = (loading) => {
    isLoading = loading;
    sendButton.disabled = loading;
    sendButton.textContent = loading ? t('Thinking...') : t('Send');
    if (chatStatus) {
      chatStatus.textContent = loading ? t('Assistant is thinking...') : t('Ready');
    }
  };

  let displayedMessages = [];
  const renderMessages = (messages) => {
    displayedMessages = messages || [];
    chatBox.innerHTML = '';
    if (!displayedMessages.length) {
      const firstName = currentUser?.user?.firstName;
      addMessage(
        firstName
          ? `${t('Hello, {name}', { name: firstName })}. ${t('Ask about your health routine, meals, activity, or progress.')}`
          : t('Start a new conversation to ask your HealthSync assistant about your day, goals, or nutrition.'),
        'bot'
      );
      return;
    }

    displayedMessages.forEach((item) => {
      addMessage(item.message, item.sender === 'user' ? 'user' : 'bot');
    });
  };

  const refreshChatHistory = async () => {
    if (!chatHistoryList) {
      return;
    }

    try {
      const response = await fetch('/api/chat/history');
      const result = await response.json();

      if (!response.ok || !result.success) {
        chatHistoryList.textContent = t('Please log in to view chat history.');
        return;
      }

      const conversations = result.conversations || [];
      if (!conversations.length) {
        chatHistoryList.textContent = t('No saved conversations yet.');
        return;
      }

      chatHistoryList.innerHTML = '';
      conversations.forEach((conversation) => {
        const row = document.createElement('div');
        row.className = 'chat-history-item';
        row.dataset.id = conversation.id;

        const button = document.createElement('button');
        button.type = 'button';
        const meta = document.createElement('div');
        meta.className = 'chat-history-meta';
        const date = document.createElement('span');
        date.textContent = new Date(conversation.updated_at).toLocaleDateString(currentLanguage);
        const count = document.createElement('span');
        count.textContent = `${conversation.messages.length} ${t('msg')}`;
        meta.append(date, count);
        const title = document.createElement('div');
        title.className = 'history-title';
        title.textContent = conversation.title || t('New chat');
        const preview = document.createElement('div');
        preview.textContent = conversation.preview || t('No messages yet.');
        button.append(meta, title, preview);
        button.addEventListener('click', () => loadConversation(conversation.id));

        const actions = document.createElement('div');
        actions.className = 'history-actions';
        const deleteButton = document.createElement('button');
        deleteButton.type = 'button';
        deleteButton.textContent = t('Delete');
        deleteButton.addEventListener('click', (event) => {
          event.stopPropagation();
          deleteConversation(conversation.id);
        });

        actions.appendChild(deleteButton);
        row.appendChild(button);
        row.appendChild(actions);
        chatHistoryList.appendChild(row);
      });
    } catch (error) {
      chatHistoryList.textContent = t('Unable to load chat history.');
    }
  };

  const loadConversation = async (sessionId) => {
    try {
      const response = await fetch('/api/chat/history', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'open', session_id: sessionId })
      });

      const result = await response.json();
      if (!response.ok || !result.success) {
        if (chatStatus) {
          chatStatus.textContent = t(result.error || 'Could not open this conversation.');
        }
        return;
      }

      window.currentChatSessionId = sessionId;
      renderMessages(result.messages || []);
      if (chatStatus) {
        chatStatus.textContent = t('Conversation loaded');
      }
    } catch (error) {
      if (chatStatus) {
        chatStatus.textContent = t('Unable to load this conversation.');
      }
    }
  };

  const deleteConversation = async (sessionId) => {
    const confirmed = window.confirm(t('Delete this conversation?'));
    if (!confirmed) {
      return;
    }

    try {
      const response = await fetch('/api/chat/history', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'delete', session_id: sessionId })
      });

      const result = await response.json();
      if (!response.ok || !result.success) {
        if (chatStatus) {
          chatStatus.textContent = t(result.error || 'Unable to delete this conversation.');
        }
        return;
      }

      if (window.currentChatSessionId === sessionId) {
        window.currentChatSessionId = null;
        renderMessages([]);
      }

      await refreshChatHistory();
    } catch (error) {
      if (chatStatus) {
        chatStatus.textContent = t('Unable to delete this conversation.');
      }
    }
  };

  const createNewChat = async () => {
    try {
      const response = await fetch('/api/chat/history', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'new' })
      });

      const result = await response.json();
      if (!response.ok || !result.success) {
        if (chatStatus) {
          chatStatus.textContent = t(result.error || 'Unable to start a new chat.');
        }
        return;
      }

      window.currentChatSessionId = result.session_id;
      renderMessages([]);
      await refreshChatHistory();
      if (chatStatus) {
        chatStatus.textContent = t('New chat started');
      }
    } catch (error) {
      if (chatStatus) {
        chatStatus.textContent = t('Unable to start a new chat.');
      }
    }
  };

  const sendMessage = async (messageText) => {
    const trimmedMessage = (messageText || chatInput.value).trim();
    if (!trimmedMessage) {
      return;
    }

    addMessage(trimmedMessage, 'user');
    chatInput.value = '';
    setLoadingState(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: trimmedMessage,
          language: currentLanguage
        })
      });

      const result = await response.json();

      if (!response.ok || !result.success) {
        addMessage(t(result.error || 'The assistant is unavailable right now. Please try again in a moment.'), 'bot');
        if (chatStatus) {
          chatStatus.textContent = t(result.error || 'Assistant unavailable.');
        }
        return;
      }

      window.currentChatSessionId = result.session_id || window.currentChatSessionId;
      addMessage(result.reply, 'bot');
      if (chatStatus) {
        chatStatus.textContent = t('Ready');
      }

      if (typeof refreshChatHistory === 'function') {
        await refreshChatHistory();
      }
    } catch (error) {
      addMessage(t('The assistant could not be reached. Please try again in a moment.'), 'bot');
      if (chatStatus) {
        chatStatus.textContent = t('Connection error. Check if Flask or Ollama is running.');
      }
    } finally {
      setLoadingState(false);
    }
  };

  sendButton.addEventListener('click', () => sendMessage(chatInput.value));

  chatInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      sendMessage(chatInput.value);
    }
  });

  quickButtons.forEach((button) => {
    button.addEventListener('click', () => {
      const question = button.dataset.question || button.textContent.trim();
      sendMessage(question);
    });
  });

  if (newChatButton) {
    newChatButton.addEventListener('click', createNewChat);
  }

  if (chatHistoryList) {
    refreshChatHistory();
  }
  window.addEventListener('healthsync:languagechange', () => {
    if (!displayedMessages.length) renderMessages([]);
    if (chatHistoryList) refreshChatHistory();
    setLoadingState(isLoading);
  });
}

function initDietTracker() {
  const dietHistoryContainer = document.getElementById('dietHistory');
  const completionValue = document.getElementById('dietCompletionValue');
  const completionText = document.getElementById('dietCompletionText');
  const progressBar = document.getElementById('dietProgressBar');
  const mealCheckboxes = document.querySelectorAll('[data-meal]');

  if (!dietHistoryContainer || !completionValue || !completionText || !progressBar) {
    return;
  }

  const mealNames = ['Breakfast', 'Lunch', 'Snacks', 'Dinner'];
  let currentStatus = null;

  const renderStatus = (payload) => {
    currentStatus = payload;
    const status = payload.status || {};
    const percentage = Number(payload.percentage || 0);
    const completed = Number(payload.completed || 0);
    const total = Number(payload.total || mealNames.length);

    completionValue.textContent = `${percentage}%`;
    completionText.textContent = t('mealCompletion', { completed, total });
    progressBar.style.width = `${percentage}%`;

    mealCheckboxes.forEach((checkbox) => {
      const mealName = checkbox.dataset.meal;
      checkbox.checked = Boolean(status[mealName]);
    });

    const historyItems = payload.history || [];
    if (!historyItems.length) {
      const row = document.createElement('div');
      row.className = 'diet-history-item';
      const value = document.createElement('strong');
      value.textContent = '0%';
      const label = document.createElement('span');
      label.textContent = t('Today');
      row.append(value, label);
      dietHistoryContainer.replaceChildren(row);
      return;
    }

    dietHistoryContainer.innerHTML = '';
    historyItems.slice(0, 5).forEach((item) => {
      const row = document.createElement('div');
      row.className = 'diet-history-item';
      const value = document.createElement('strong');
      value.textContent = `${item.percentage}%`;
      const label = document.createElement('span');
      label.textContent = item.date;
      row.append(value, label);
      dietHistoryContainer.appendChild(row);
    });
  };

  const fetchStatus = async (date) => {
    try {
      const response = await fetch(`/api/diet/status?date=${encodeURIComponent(date)}`);
      const result = await response.json();
      if (!response.ok || !result.success) {
        console.error('Unable to fetch diet status:', result.error || response.statusText);
        return null;
      }
      return result;
    } catch (error) {
      console.error('Unable to fetch diet status:', error);
      return null;
    }
  };

  const saveMealStatus = async (mealName, checked) => {
    const today = new Date().toISOString().slice(0, 10);
    const response = await fetch('/api/diet/status', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        date: today,
        meal: mealName,
        completed: checked
      })
    });

    const result = await response.json();
    if (response.ok && result.success) {
      renderStatus(result);
    } else {
      console.error('Unable to save diet status:', result.error || response.statusText);
    }
  };

  mealCheckboxes.forEach((checkbox) => {
    checkbox.addEventListener('change', async () => {
      await saveMealStatus(checkbox.dataset.meal, checkbox.checked);
    });
  });

  const today = new Date().toISOString().slice(0, 10);
  fetchStatus(today).then((result) => {
    if (result) {
      renderStatus(result);
    }
  });
  window.addEventListener('healthsync:languagechange', () => {
    if (currentStatus) renderStatus(currentStatus);
  });
}

function initActivityTracker() {
  const completionValue = document.getElementById('activityCompletionValue');
  const completionText = document.getElementById('activityCompletionText');
  const progressBar = document.getElementById('activityProgressBar');
  const checkboxes = document.querySelectorAll('[data-activity]');
  if (!completionValue || !completionText || !progressBar || !checkboxes.length) return;

  let currentStatus = null;
  const render = (result) => {
    currentStatus = result;
    completionValue.textContent = `${result.percentage}%`;
    completionText.textContent = t('activityCompletion', {
      completed: result.completed,
      total: result.total
    });
    progressBar.style.width = `${result.percentage}%`;
    checkboxes.forEach((checkbox) => {
      checkbox.checked = Boolean(result.status[checkbox.dataset.activity]);
    });
  };

  const today = new Date().toISOString().slice(0, 10);
  fetch(`/api/activity/status?date=${encodeURIComponent(today)}`)
    .then(async (response) => {
      const result = await response.json();
      if (!response.ok || !result.success) {
        throw new Error(result.error || response.statusText);
      }
      render(result);
    })
    .catch((error) => console.error('Unable to load activity status:', error));

  checkboxes.forEach((checkbox) => {
    checkbox.addEventListener('change', async () => {
      try {
        const response = await fetch('/api/activity/status', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            date: today,
            activity: checkbox.dataset.activity,
            completed: checkbox.checked
          })
        });
        const result = await response.json();
        if (!response.ok || !result.success) {
          throw new Error(result.error || response.statusText);
        }
        render(result);
      } catch (error) {
        checkbox.checked = !checkbox.checked;
        console.error('Unable to save activity status:', error);
      }
    });
  });
  window.addEventListener('healthsync:languagechange', () => {
    if (currentStatus) render(currentStatus);
  });
}

function medicalNode(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined && text !== null) node.textContent = text;
  return node;
}

function medicalDateLabel(value) {
  if (!value) return t('Not recorded');
  const date = new Date(`${value.slice(0, 10)}T00:00:00`);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleDateString(
    { en: 'en-US', te: 'te-IN', hi: 'hi-IN' }[currentLanguage] || 'en-US',
    { year: 'numeric', month: 'short', day: 'numeric' }
  );
}

async function medicalRequest(url, options = {}) {
  const response = await fetch(url, options);
  const result = await response.json();
  if (!response.ok || !result.success) {
    throw new Error(result.error || response.statusText || t('Could not load medical records. Please sign in again.'));
  }
  return result;
}

function medicalFormJson(form) {
  return Object.fromEntries(new FormData(form).entries());
}

function setMedicalStatus(id, message, isError = false) {
  const status = document.getElementById(id);
  if (!status) return;
  status.textContent = message;
  status.classList.toggle('is-error', isError);
}

function medicalErrorText(error) {
  return t(error instanceof Error ? error.message : String(error || 'Medical records could not be loaded.'));
}

function renderMedicalEmpty(container) {
  container.replaceChildren(medicalNode('p', 'medical-empty', t('No records yet. Add your first entry above.')));
}

function initMedicalPage() {
  if (!document.getElementById('medicalHistoryForm')) return;
  if (!currentUser) {
    window.location.replace('/login.html');
    return;
  }

  let medicalData = null;
  const historyForm = document.getElementById('medicalHistoryForm');
  const treatmentForm = document.getElementById('treatmentForm');
  const medicationForm = document.getElementById('medicationForm');
  const reportForm = document.getElementById('reportForm');
  const readingForm = document.getElementById('readingForm');
  const assistantForm = document.getElementById('medicalAssistantForm');
  const reportVerification = document.getElementById('reportVerification');

  const refresh = async () => {
    medicalData = await medicalRequest('/api/medical');
    const history = medicalData.history;
    historyForm.elements.hasPreviousDiabetes.value = history.hasPreviousDiabetes ? 'yes' : 'no';
    historyForm.elements.hasPreviousTreatment.value = history.hasPreviousTreatment ? 'yes' : 'no';
    historyForm.elements.diagnosisDate.value = history.diagnosisDate || '';
    historyForm.elements.yearsWithDiabetes.value = history.yearsWithDiabetes ?? '';
    historyForm.elements.diabetesCategory.value = history.diabetesCategory || '';
    historyForm.elements.complications.value = history.complications || '';
    document.getElementById('reportConsent').checked = history.reportsConsent;
    renderMedicalRecords();
  };

  const renderTreatments = () => {
    const list = document.getElementById('treatmentList');
    list.replaceChildren();
    if (!medicalData.treatments.length) return renderMedicalEmpty(list);
    medicalData.treatments.forEach((record) => {
      const row = medicalNode('article', 'medical-record-row');
      const details = medicalNode('div', 'medical-record-copy');
      details.append(
        medicalNode('strong', '', record.treatment_details),
        medicalNode('span', '', record.provider_name || t('Not recorded')),
        medicalNode('small', '', `${medicalDateLabel(record.started_on)} – ${medicalDateLabel(record.ended_on)}`)
      );
      const actions = medicalNode('div', 'medical-record-actions');
      const edit = medicalNode('button', 'btn btn-outline btn-small', t('Edit'));
      edit.type = 'button';
      edit.addEventListener('click', () => {
        treatmentForm.elements.recordId.value = record.id;
        treatmentForm.elements.details.value = record.treatment_details;
        treatmentForm.elements.provider.value = record.provider_name || '';
        treatmentForm.elements.startedOn.value = record.started_on || '';
        treatmentForm.elements.endedOn.value = record.ended_on || '';
        treatmentForm.querySelector('[type="submit"]').textContent = t('Update treatment');
        treatmentForm.querySelector('[data-cancel-treatment]').hidden = false;
        treatmentForm.scrollIntoView({ behavior: 'smooth', block: 'center' });
      });
      const remove = medicalNode('button', 'btn btn-outline btn-small', t('Delete'));
      remove.type = 'button';
      remove.addEventListener('click', async () => {
        if (!window.confirm(t('Please confirm before deleting this record.'))) return;
        try {
          await medicalRequest(`/api/medical/treatments/${record.id}`, { method: 'DELETE' });
          await refresh();
        } catch (error) {
          setMedicalStatus('treatmentStatus', medicalErrorText(error), true);
        }
      });
      actions.append(edit, remove);
      row.append(details, actions);
      list.appendChild(row);
    });
  };

  const resetMedicationForm = () => {
    medicationForm.reset();
    medicationForm.elements.recordId.value = '';
    medicationForm.elements.isCurrent.value = 'yes';
    medicationForm.querySelector('[type="submit"]').textContent = t('Save medication');
    medicationForm.querySelector('[data-cancel-medication]').hidden = true;
  };

  const renderMedications = () => {
    const list = document.getElementById('medicationList');
    list.replaceChildren();
    if (!medicalData.medications.length) return renderMedicalEmpty(list);
    medicalData.medications.forEach((record) => {
      const row = medicalNode('article', 'medical-record-row');
      const details = medicalNode('div', 'medical-record-copy');
      const medicationMeta = [record.dosage, record.frequency, record.duration].filter(Boolean).join(' · ');
      details.append(
        medicalNode('strong', '', record.medication_name),
        medicalNode('span', '', medicationMeta || t('Not recorded')),
        medicalNode('small', '', `${medicalDateLabel(record.started_on)} · ${record.is_current ? t('Currently taking') : t('Discontinued')}${record.discontinued_on ? ` · ${medicalDateLabel(record.discontinued_on)}` : ''}`)
      );
      if (!record.is_current && record.discontinuation_reason) {
        details.appendChild(medicalNode('small', '', record.discontinuation_reason));
      }
      const actions = medicalNode('div', 'medical-record-actions');
      const edit = medicalNode('button', 'btn btn-outline btn-small', t('Edit'));
      edit.type = 'button';
      edit.addEventListener('click', () => {
        medicationForm.elements.recordId.value = record.id;
        medicationForm.elements.name.value = record.medication_name;
        medicationForm.elements.dosage.value = record.dosage;
        medicationForm.elements.frequency.value = record.frequency;
        medicationForm.elements.startedOn.value = record.started_on || '';
        medicationForm.elements.duration.value = record.duration;
        medicationForm.elements.isCurrent.value = record.is_current ? 'yes' : 'no';
        medicationForm.elements.discontinuedOn.value = record.discontinued_on || '';
        medicationForm.elements.discontinuationReason.value = record.discontinuation_reason || '';
        medicationForm.querySelector('[type="submit"]').textContent = t('Update medication');
        medicationForm.querySelector('[data-cancel-medication]').hidden = false;
        medicationForm.scrollIntoView({ behavior: 'smooth', block: 'center' });
      });
      const remove = medicalNode('button', 'btn btn-outline btn-small', t('Delete'));
      remove.type = 'button';
      remove.addEventListener('click', async () => {
        if (!window.confirm(t('Please confirm before deleting this record.'))) return;
        try {
          await medicalRequest(`/api/medical/medications/${record.id}`, { method: 'DELETE' });
          await refresh();
        } catch (error) {
          setMedicalStatus('medicationStatus', medicalErrorText(error), true);
        }
      });
      actions.append(edit, remove);
      row.append(details, actions);
      list.appendChild(row);
    });
  };

  const readingsForReport = (reportId) => medicalData.readings.filter(
    (reading) => Number(reading.report_id) === Number(reportId)
  );

  const openVerification = (report, suggestions = {}) => {
    reportVerification.replaceChildren();
    reportVerification.hidden = false;
    const heading = medicalNode('h3', '', t('Review extracted results'));
    const note = medicalNode('p', '', t('Check each value against your report. Values are not saved until you confirm them.'));
    const form = medicalNode('form', 'form-grid medical-verify-form');
    form.dataset.reportId = report.id;
    const dateLabel = medicalNode('label', '', t('Test date'));
    dateLabel.htmlFor = 'verifyTestDate';
    const dateField = medicalNode('input');
    dateField.id = 'verifyTestDate';
    dateField.name = 'testDate';
    dateField.type = 'date';
    dateField.required = true;
    dateField.value = suggestions.testDate || report.testDate || '';
    const dateWrap = medicalNode('div', 'field');
    dateWrap.append(dateLabel, dateField);

    const facilityLabel = medicalNode('label', '', t('Hospital or laboratory'));
    facilityLabel.htmlFor = 'verifyFacility';
    const facilityField = medicalNode('input');
    facilityField.id = 'verifyFacility';
    facilityField.name = 'facilityName';
    facilityField.maxLength = 300;
    facilityField.value = report.facilityName || '';
    const facilityWrap = medicalNode('div', 'field');
    facilityWrap.append(facilityLabel, facilityField);
    form.append(dateWrap, facilityWrap);

    const readingLabels = {
      fasting: 'Fasting blood glucose',
      postprandial: 'Postprandial blood glucose (PP)',
      random: 'Random blood glucose',
      hba1c: 'HbA1c'
    };
    const existingReadings = readingsForReport(report.id);
    Object.entries(readingLabels).forEach(([kind, labelText]) => {
      const existing = existingReadings.find((item) => item.measurement_type === kind);
      const suggested = suggestions[kind] ?? existing?.value ?? '';
      const wrap = medicalNode('div', 'medical-confirm-field');
      const label = medicalNode('label', '', t(labelText));
      const controls = medicalNode('div', 'medical-confirm-controls');
      const checkbox = medicalNode('input');
      checkbox.type = 'checkbox';
      checkbox.name = `confirmed-${kind}`;
      checkbox.checked = Boolean(existing);
      const input = medicalNode('input');
      input.name = kind;
      input.type = 'number';
      input.min = '1';
      input.max = kind === 'hba1c' ? '30' : '2000';
      input.step = '0.1';
      input.value = suggested;
      input.setAttribute('aria-label', t(labelText));
      const unit = medicalNode('span', 'medical-unit', kind === 'hba1c' ? '%' : 'mg/dL');
      controls.append(checkbox, input, unit);
      wrap.append(label, controls);
      const reported = suggestions.reportedValues?.[kind];
      if (reported) {
        const sourceValue = medicalNode(
          'small',
          'medical-source-value',
          t('Report value: {value} {unit}', {
            value: reported.value,
            unit: reported.unit || t('Unit not shown')
          })
        );
        wrap.appendChild(sourceValue);
      }
      form.appendChild(wrap);
    });

    const otherLabel = medicalNode('label', '', t('Other test results'));
    otherLabel.htmlFor = 'verifyOtherResults';
    const otherField = medicalNode('textarea');
    otherField.id = 'verifyOtherResults';
    otherField.name = 'otherResults';
    otherField.rows = 3;
    otherField.maxLength = 4000;
    otherField.value = report.otherResults || '';
    const otherWrap = medicalNode('div', 'field medical-span-two');
    otherWrap.append(otherLabel, otherField);
    const status = medicalNode('p', 'medical-status');
    status.id = 'verificationStatus';
    status.setAttribute('role', 'status');
    const actions = medicalNode('div', 'medical-form-actions medical-span-two');
    const submit = medicalNode('button', 'btn btn-primary', t('Confirm selected results'));
    submit.type = 'submit';
    const close = medicalNode('button', 'btn btn-outline', t('Cancel edit'));
    close.type = 'button';
    close.addEventListener('click', () => {
      reportVerification.hidden = true;
      reportVerification.replaceChildren();
    });
    actions.append(submit, close, status);
    form.append(otherWrap, actions);
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const payload = {
        testDate: form.elements.testDate.value,
        facilityName: form.elements.facilityName.value,
        otherResults: form.elements.otherResults.value,
        confirmed: {}
      };
      Object.keys(readingLabels).forEach((kind) => {
        payload.confirmed[kind] = form.elements[`confirmed-${kind}`].checked;
        payload[kind] = form.elements[kind].value;
      });
      submit.disabled = true;
      try {
        await medicalRequest(`/api/medical/reports/${report.id}/verify`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        reportVerification.hidden = true;
        reportVerification.replaceChildren();
        setMedicalStatus('reportStatus', t('Medical records saved.'));
        await refresh();
      } catch (error) {
        status.textContent = medicalErrorText(error);
        status.classList.add('is-error');
      } finally {
        submit.disabled = false;
      }
    });
    reportVerification.append(heading, note, form);
    reportVerification.scrollIntoView({ behavior: 'smooth', block: 'center' });
  };

  const renderReports = () => {
    const list = document.getElementById('reportList');
    list.replaceChildren();
    if (!medicalData.reports.length) renderMedicalEmpty(list);
    medicalData.reports.forEach((report) => {
      const row = medicalNode('article', 'medical-record-row medical-report-row');
      const details = medicalNode('div', 'medical-record-copy');
      details.append(
        medicalNode('strong', '', report.name),
        medicalNode('span', '', t(report.category === 'before_treatment' ? 'Before Treatment / Previous Reports' : 'After Treatment / Latest Reports')),
        medicalNode('small', '', `${t('Upload date')}: ${medicalDateLabel(report.uploadedAt)} · ${t('Test date')}: ${medicalDateLabel(report.testDate)}`)
      );
      const badge = medicalNode('span', `badge ${report.verified ? 'success' : 'warning'}`, t(report.verified ? 'Verified' : 'Unverified'));
      details.appendChild(badge);
      const actions = medicalNode('div', 'medical-record-actions');
      const view = medicalNode('a', 'btn btn-outline btn-small', t('View'));
      view.href = `/api/medical/reports/${report.id}/file`;
      view.target = '_blank';
      view.rel = 'noopener noreferrer';
      const download = medicalNode('a', 'btn btn-outline btn-small', t('Download'));
      download.href = `/api/medical/reports/${report.id}/file?download=1`;
      const verify = medicalNode('button', 'btn btn-outline btn-small', t(report.verified ? 'Edit' : 'Review extracted results'));
      verify.type = 'button';
      verify.addEventListener('click', () => openVerification(report));
      const remove = medicalNode('button', 'btn btn-outline btn-small', t('Delete'));
      remove.type = 'button';
      remove.addEventListener('click', async () => {
        if (!window.confirm(t('Please confirm before deleting this report.'))) return;
        try {
          await medicalRequest(`/api/medical/reports/${report.id}`, { method: 'DELETE' });
          await refresh();
        } catch (error) {
          setMedicalStatus('reportStatus', medicalErrorText(error), true);
        }
      });
      actions.append(view, download, verify, remove);
      row.append(details, actions);
      list.appendChild(row);
    });
    populateReportComparison();
  };

  const populateReportComparison = () => {
    const selectA = document.getElementById('compareReportA');
    const selectB = document.getElementById('compareReportB');
    [selectA, selectB].forEach((select) => {
      const previous = select.value;
      select.replaceChildren();
      medicalData.reports.filter((report) => report.verified).forEach((report) => {
        const option = document.createElement('option');
        option.value = report.id;
        option.textContent = `${report.name} · ${medicalDateLabel(report.testDate)}`;
        select.appendChild(option);
      });
      if ([...select.options].some((option) => option.value === previous)) select.value = previous;
    });
  };

  const renderSelectedReportComparison = () => {
    const target = document.getElementById('selectedReportComparison');
    target.replaceChildren();
    const selectedA = medicalData.reports.find((report) => String(report.id) === document.getElementById('compareReportA').value);
    const selectedB = medicalData.reports.find((report) => String(report.id) === document.getElementById('compareReportB').value);
    if (!selectedA || !selectedB || selectedA.id === selectedB.id) {
      target.appendChild(medicalNode('p', 'medical-empty', t('No readings recorded')));
      return;
    }
    const [reportA, reportB] = [selectedA, selectedB].sort(
      (a, b) => (a.testDate || a.uploadedAt).localeCompare(b.testDate || b.uploadedAt)
    );
    const readingsA = readingsForReport(reportA.id);
    const readingsB = readingsForReport(reportB.id);
    const labels = {
      fasting: 'Fasting blood glucose',
      postprandial: 'Postprandial blood glucose (PP)',
      random: 'Random blood glucose',
      hba1c: 'HbA1c'
    };
    Object.entries(labels).forEach(([kind, label]) => {
      const previous = readingsA.find((reading) => reading.measurement_type === kind);
      const latest = readingsB.find((reading) => reading.measurement_type === kind);
      const comparison = medicalNode('div', 'selected-comparison-item');
      comparison.append(
        medicalNode('strong', '', t(label)),
        medicalNode('span', '', `${reportA.name} (${medicalDateLabel(reportA.testDate)}): ${previous ? `${previous.value} ${previous.unit}` : t('Not recorded')}`),
        medicalNode('span', '', `${reportB.name} (${medicalDateLabel(reportB.testDate)}): ${latest ? `${latest.value} ${latest.unit}` : t('Not recorded')}`)
      );
      if (previous && latest) {
        const difference = Number(latest.value) - Number(previous.value);
        comparison.appendChild(medicalNode(
          'span',
          '',
          `${t('Difference')}: ${difference > 0 ? '+' : ''}${difference.toFixed(1)} ${latest.unit}`
        ));
      }
      target.appendChild(comparison);
    });
  };

  const renderReadings = () => {
    const list = document.getElementById('readingList');
    list.replaceChildren();
    if (!medicalData.readings.length) return renderMedicalEmpty(list);
    const labels = {
      fasting: 'Fasting blood glucose',
      postprandial: 'Postprandial blood glucose (PP)',
      random: 'Random blood glucose',
      hba1c: 'HbA1c'
    };
    medicalData.readings.forEach((reading) => {
      const row = medicalNode('article', 'medical-record-row');
      const time = reading.measurement_time ? ` ${reading.measurement_time.slice(0, 5)}` : '';
      const source = reading.source === 'report' ? t('Uploaded reports') : t('Manual entry');
      const details = medicalNode('div', 'medical-record-copy');
      details.append(
        medicalNode('strong', '', `${t(labels[reading.measurement_type])}: ${reading.value} ${reading.unit}`),
        medicalNode('small', '', `${medicalDateLabel(reading.measurement_date)}${time} · ${source}`)
      );
      const actions = medicalNode('div', 'medical-record-actions');
      if (reading.source === 'manual') {
        const edit = medicalNode('button', 'btn btn-outline btn-small', t('Edit'));
        edit.type = 'button';
        edit.addEventListener('click', () => {
          readingForm.dataset.readingId = reading.id;
          readingForm.elements.type.value = reading.measurement_type;
          readingForm.elements.value.value = reading.value;
          readingForm.elements.measuredAt.value = reading.measurement_time
            ? `${reading.measurement_date}T${reading.measurement_time.slice(0, 5)}`
            : '';
          readingForm.querySelector('[type="submit"]').textContent = t('Update reading');
          readingForm.querySelector('[data-cancel-reading]').hidden = false;
          readingForm.scrollIntoView({ behavior: 'smooth', block: 'center' });
        });
        const remove = medicalNode('button', 'btn btn-outline btn-small', t('Delete'));
        remove.type = 'button';
        remove.addEventListener('click', async () => {
          if (!window.confirm(t('Please confirm before deleting this record.'))) return;
          try {
            await medicalRequest(`/api/medical/readings/${reading.id}`, { method: 'DELETE' });
            await refresh();
          } catch (error) {
            setMedicalStatus('readingStatus', medicalErrorText(error), true);
          }
        });
        actions.append(edit, remove);
      } else {
        const correct = medicalNode('button', 'btn btn-outline btn-small', t('Review extracted results'));
        correct.type = 'button';
        correct.addEventListener('click', () => {
          const report = medicalData.reports.find((item) => item.id === reading.report_id);
          if (report) openVerification(report);
        });
        actions.append(correct);
      }
      row.append(details, actions);
      list.appendChild(row);
    });
  };

  const renderComparison = () => {
    const target = document.getElementById('readingComparison');
    target.replaceChildren();
    const labels = {
      fasting: 'Fasting blood glucose',
      postprandial: 'Postprandial blood glucose (PP)',
      random: 'Random blood glucose',
      hba1c: 'HbA1c'
    };
    Object.entries(labels).forEach(([kind, label]) => {
      const series = [...medicalData.readings]
        .filter((reading) => reading.measurement_type === kind)
        .sort((a, b) => `${a.measurement_date} ${a.measurement_time || ''}`.localeCompare(`${b.measurement_date} ${b.measurement_time || ''}`));
        const previous = series.length > 1 ? series[0] : null;
        const latest = series.length ? series[series.length - 1] : null;
      const difference = previous && latest ? Number(latest.value) - Number(previous.value) : null;
      const direction = difference === null
        ? t('Not recorded')
        : difference === 0
          ? t('Direction: unchanged')
          : difference < 0
            ? t('Direction: lower')
            : t('Direction: higher');
      const item = medicalNode('article', 'comparison-metric');
      item.appendChild(medicalNode('h3', '', t(label)));
      const values = medicalNode('div', 'comparison-values');
      const previousBlock = medicalNode('div', '');
      previousBlock.append(
        medicalNode('small', '', t('Previous value')),
        medicalNode('strong', '', previous ? `${previous.value} ${previous.unit}` : t('Not recorded')),
        medicalNode('small', '', previous ? medicalDateLabel(previous.measurement_date) : '')
      );
      const latestBlock = medicalNode('div', '');
      latestBlock.append(
        medicalNode('small', '', t('Latest value')),
        medicalNode('strong', '', latest ? `${latest.value} ${latest.unit}` : t('Not recorded')),
        medicalNode('small', '', latest ? medicalDateLabel(latest.measurement_date) : '')
      );
      values.append(previousBlock, latestBlock);
      item.appendChild(values);
      const deltaText = previous && latest
        ? `${t('Difference')}: ${difference > 0 ? '+' : ''}${difference.toFixed(1)} ${latest.unit}${Number(previous.value) !== 0 ? ` (${((difference / Number(previous.value)) * 100).toFixed(1)}%)` : ''}`
        : t('Not recorded');
      item.append(
        medicalNode('span', 'comparison-delta', deltaText),
        medicalNode('span', 'comparison-direction', `${t('Change direction only')}: ${direction}`)
      );
      target.appendChild(item);
    });
    renderReadingChart();
    renderTreatmentComparison();
  };

  const renderReadingChart = () => {
    const chart = document.getElementById('readingChart');
    chart.replaceChildren();
    const types = ['fasting', 'postprandial', 'random', 'hba1c'];
    const labels = {
      fasting: 'Fasting blood glucose',
      postprandial: 'Postprandial blood glucose (PP)',
      random: 'Random blood glucose',
      hba1c: 'HbA1c'
    };
    types.forEach((kind) => {
      const values = [...medicalData.readings]
        .filter((reading) => reading.measurement_type === kind)
        .sort((a, b) => `${a.measurement_date} ${a.measurement_time || ''}`.localeCompare(`${b.measurement_date} ${b.measurement_time || ''}`));
      if (!values.length) return;
      const figure = medicalNode('figure', 'medical-chart-figure');
      figure.appendChild(medicalNode('figcaption', '', t(labels[kind])));
      const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.setAttribute('viewBox', '0 0 640 230');
      svg.setAttribute('role', 'img');
      svg.setAttribute('aria-label', t(labels[kind]));
      const numeric = values.map((reading) => Number(reading.value));
      const min = Math.min(...numeric);
      const max = Math.max(...numeric);
      const span = max - min || Math.max(max * 0.15, 1);
      const points = values.map((reading, index) => ({
        x: values.length === 1 ? 320 : 54 + (index / (values.length - 1)) * 532,
        y: 174 - ((Number(reading.value) - min) / span) * 126,
        reading
      }));
      [48, 111, 174].forEach((y) => {
        const grid = document.createElementNS(svg.namespaceURI, 'line');
        grid.setAttribute('x1', '48');
        grid.setAttribute('x2', '592');
        grid.setAttribute('y1', String(y));
        grid.setAttribute('y2', String(y));
        grid.setAttribute('class', 'chart-grid-line');
        svg.appendChild(grid);
      });
      if (points.length > 1) {
        const line = document.createElementNS(svg.namespaceURI, 'polyline');
        line.setAttribute('points', points.map((point) => `${point.x},${point.y}`).join(' '));
        line.setAttribute('class', 'chart-series-line');
        svg.appendChild(line);
      }
      points.forEach((point, index) => {
        const dot = document.createElementNS(svg.namespaceURI, 'circle');
        dot.setAttribute('cx', String(point.x));
        dot.setAttribute('cy', String(point.y));
        dot.setAttribute('r', '5');
        dot.setAttribute('class', 'chart-series-point');
        const title = document.createElementNS(svg.namespaceURI, 'title');
        title.textContent = `${point.reading.value} ${point.reading.unit} · ${medicalDateLabel(point.reading.measurement_date)}`;
        dot.appendChild(title);
        svg.appendChild(dot);
        const valueText = document.createElementNS(svg.namespaceURI, 'text');
        valueText.setAttribute('x', String(point.x));
        valueText.setAttribute('y', String(point.y - 10));
        valueText.setAttribute('text-anchor', 'middle');
        valueText.setAttribute('class', 'chart-value-label');
        valueText.textContent = String(point.reading.value);
        svg.appendChild(valueText);
        const dateText = document.createElementNS(svg.namespaceURI, 'text');
        dateText.setAttribute('x', String(point.x));
        dateText.setAttribute('y', '210');
        dateText.setAttribute('text-anchor', 'middle');
        dateText.setAttribute('class', 'chart-date-label');
        if (index === 0 || index === points.length - 1) {
          dateText.textContent = medicalDateLabel(point.reading.measurement_date);
          svg.appendChild(dateText);
        }
      });
      figure.appendChild(svg);
      chart.appendChild(figure);
    });
    if (!chart.childElementCount) renderMedicalEmpty(chart);
  };

  const renderTreatmentComparison = () => {
    const target = document.getElementById('treatmentComparison');
    target.replaceChildren();
    const current = medicalData.medications.filter((item) => item.is_current);
    const previous = medicalData.treatments[0];
    const previousColumn = medicalNode('div', 'treatment-column');
    previousColumn.appendChild(medicalNode('strong', '', t('Previous Treatment')));
    previousColumn.appendChild(medicalNode('p', '', previous?.treatment_details || t('Not recorded')));
    const currentColumn = medicalNode('div', 'treatment-column');
    currentColumn.appendChild(medicalNode('strong', '', t('Current')));
    currentColumn.appendChild(medicalNode('p', '', current.length
      ? current.map((item) => [item.medication_name, item.dosage, item.frequency].filter(Boolean).join(' · ')).join('; ')
      : t('Not recorded')));
    target.append(previousColumn, currentColumn);
  };

  const renderTimeline = () => {
    const target = document.getElementById('medicalTimeline');
    target.replaceChildren();
    if (!medicalData.timeline.length) {
      return renderMedicalEmpty(target);
    }
    const titleKeys = {
      diagnosis: 'Diabetes diagnosis',
      treatment: 'Treatment history',
      medication: 'Medication change',
      report: 'Medical report',
      reading: 'Blood glucose reading'
    };
    medicalData.timeline.forEach((event) => {
      const item = medicalNode('article', `medical-timeline-item kind-${event.kind}`);
      item.append(
        medicalNode('time', '', medicalDateLabel(event.date)),
        medicalNode('strong', '', t(titleKeys[event.kind] || event.title)),
        medicalNode('span', '', event.detail || t('Not recorded'))
      );
      target.appendChild(item);
    });
  };

  function renderMedicalRecords() {
    renderTreatments();
    renderMedications();
    renderReports();
    renderReadings();
    renderComparison();
    renderTimeline();
  }

  historyForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const form = medicalFormJson(historyForm);
    try {
      await medicalRequest('/api/medical/history', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          hasPreviousDiabetes: form.hasPreviousDiabetes === 'yes',
          hasPreviousTreatment: form.hasPreviousTreatment === 'yes',
          diagnosisDate: form.diagnosisDate,
          yearsWithDiabetes: form.yearsWithDiabetes,
          diabetesCategory: form.diabetesCategory,
          complications: form.complications
        })
      });
      setMedicalStatus('historyStatus', t('Medical records saved.'));
      await refresh();
    } catch (error) {
      setMedicalStatus('historyStatus', medicalErrorText(error), true);
    }
  });

  const resetTreatmentForm = () => {
    treatmentForm.reset();
    treatmentForm.elements.recordId.value = '';
    treatmentForm.querySelector('[type="submit"]').textContent = t('Save treatment');
    treatmentForm.querySelector('[data-cancel-treatment]').hidden = true;
  };
  treatmentForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const form = medicalFormJson(treatmentForm);
    const recordId = form.recordId;
    try {
      await medicalRequest(recordId ? `/api/medical/treatments/${recordId}` : '/api/medical/treatments', {
        method: recordId ? 'PUT' : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form)
      });
      resetTreatmentForm();
      setMedicalStatus('treatmentStatus', t('Medical records saved.'));
      await refresh();
    } catch (error) {
      setMedicalStatus('treatmentStatus', medicalErrorText(error), true);
    }
  });
  treatmentForm.querySelector('[data-cancel-treatment]').addEventListener('click', resetTreatmentForm);

  medicationForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const form = medicalFormJson(medicationForm);
    const recordId = form.recordId;
    const payload = {
      name: form.name,
      dosage: form.dosage,
      frequency: form.frequency,
      startedOn: form.startedOn,
      duration: form.duration,
      isCurrent: form.isCurrent === 'yes',
      discontinuedOn: form.discontinuedOn,
      discontinuationReason: form.discontinuationReason
    };
    try {
      await medicalRequest(recordId ? `/api/medical/medications/${recordId}` : '/api/medical/medications', {
        method: recordId ? 'PUT' : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      resetMedicationForm();
      setMedicalStatus('medicationStatus', t('Medical records saved.'));
      await refresh();
    } catch (error) {
      setMedicalStatus('medicationStatus', medicalErrorText(error), true);
    }
  });
  medicationForm.querySelector('[data-cancel-medication]').addEventListener('click', resetMedicationForm);

  document.getElementById('reportConsent').addEventListener('change', async (event) => {
    const checkbox = event.currentTarget;
    checkbox.disabled = true;
    try {
      await medicalRequest('/api/medical/consent', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ consent: checkbox.checked })
      });
      medicalData.history.reportsConsent = checkbox.checked;
      setMedicalStatus('reportStatus', t('Medical records saved.'));
    } catch (error) {
      checkbox.checked = !checkbox.checked;
      setMedicalStatus('reportStatus', medicalErrorText(error), true);
    } finally {
      checkbox.disabled = false;
    }
  });

  reportForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!document.getElementById('reportConsent').checked) {
      setMedicalStatus('reportStatus', t('Report processing consent is required before upload.'), true);
      return;
    }
    const submit = reportForm.querySelector('[type="submit"]');
    submit.disabled = true;
    submit.textContent = t('Saving…');
    try {
      const response = await fetch('/api/medical/reports', {
        method: 'POST',
        body: new FormData(reportForm)
      });
      const result = await response.json();
      if (!response.ok || !result.success) throw new Error(result.error || response.statusText);
      setMedicalStatus('reportStatus', t('Report uploaded. Review the extracted values below.'));
      const suggestions = result.extraction?.values || {};
      if (!result.extraction?.success) {
        setMedicalStatus('reportStatus', t('No readable text was extracted. You can enter values from your report below.'));
      }
      const report = {
        ...result.report,
        facilityName: reportForm.elements.facilityName.value
      };
      reportForm.reset();
      reportForm.elements.category.value = 'before_treatment';
      openVerification(report, suggestions);
      await refresh();
    } catch (error) {
      setMedicalStatus('reportStatus', medicalErrorText(error), true);
    } finally {
      submit.disabled = false;
      submit.textContent = t('Upload and extract text locally');
    }
  });

  document.getElementById('compareReportsButton').addEventListener('click', renderSelectedReportComparison);
  document.getElementById('compareReportA').addEventListener('change', renderSelectedReportComparison);
  document.getElementById('compareReportB').addEventListener('change', renderSelectedReportComparison);

  readingForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const form = medicalFormJson(readingForm);
    const recordId = readingForm.dataset.readingId;
    const payload = { type: form.type, value: form.value, measuredAt: form.measuredAt };
    try {
      await medicalRequest(recordId ? `/api/medical/readings/${recordId}` : '/api/medical/readings', {
        method: recordId ? 'PUT' : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      readingForm.reset();
      delete readingForm.dataset.readingId;
      readingForm.querySelector('[type="submit"]').textContent = t('Add reading');
      readingForm.querySelector('[data-cancel-reading]').hidden = true;
      setMedicalStatus('readingStatus', t('Medical records saved.'));
      await refresh();
    } catch (error) {
      setMedicalStatus('readingStatus', medicalErrorText(error), true);
    }
  });
  readingForm.querySelector('[data-cancel-reading]').addEventListener('click', () => {
    readingForm.reset();
    delete readingForm.dataset.readingId;
    readingForm.querySelector('[type="submit"]').textContent = t('Add reading');
    readingForm.querySelector('[data-cancel-reading]').hidden = true;
  });
  document.getElementById('readingType').addEventListener('change', (event) => {
    const input = document.getElementById('readingValue');
    input.max = event.currentTarget.value === 'hba1c' ? '30' : '2000';
  });

  assistantForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const status = document.getElementById('medicalAssistantStatus');
    const answer = document.getElementById('medicalAssistantAnswer');
    const submit = assistantForm.querySelector('[type="submit"]');
    status.textContent = t('Saving…');
    status.classList.remove('is-error');
    answer.textContent = '';
    submit.disabled = true;
    try {
      const result = await medicalRequest('/api/medical/assistant', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: assistantForm.elements.question.value })
      });
      status.textContent = '';
      answer.textContent = result.answer;
    } catch (error) {
      status.textContent = error.message.includes('Ollama') || error.message.includes('llama3.2')
        ? t('A local AI explanation is unavailable right now. Check that Ollama and llama3.2:3b are running.')
        : medicalErrorText(error);
      status.classList.add('is-error');
    } finally {
      submit.disabled = false;
    }
  });

  window.addEventListener('healthsync:languagechange', () => {
    if (medicalData) renderMedicalRecords();
    const readingId = readingForm.dataset.readingId;
    readingForm.querySelector('[type="submit"]').textContent = t(readingId ? 'Update reading' : 'Add reading');
  });

  refresh().catch((error) => {
    setMedicalStatus('historyStatus', medicalErrorText(error) || t('Could not load medical records. Please sign in again.'), true);
  });
}

document.addEventListener('DOMContentLoaded', () => {
  setActiveNav();
  setupMobileNav();
  initFormFeedback();
  initSwitches();
  initLanguageSelector();
  initYear();
  initAuthForms();
  initDietTracker();
  initActivityTracker();
  loadCurrentUser().then(() => {
    initProfilePage();
    initDashboard();
    initProgressTracker();
    initAiAssistant();
    initMedicalPage();
  });
});
