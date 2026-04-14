(function () {
  function clone(value) {
    return JSON.parse(JSON.stringify(value));
  }

  function payload() {
    return window.KA_WORKFLOW_PAYLOAD || {};
  }

  function readJson(key, fallback) {
    try {
      return JSON.parse(localStorage.getItem(key) || JSON.stringify(fallback));
    } catch (_err) {
      return clone(fallback);
    }
  }

  function writeJson(key, value) {
    localStorage.setItem(key, JSON.stringify(value));
    return value;
  }

  function removeKey(key) {
    localStorage.removeItem(key);
    return null;
  }

  function bootstrappedRegistrations() {
    return clone(payload().registrations || []);
  }

  function bootstrappedSubmissions() {
    return clone(payload().intake_submissions || []);
  }

  function currentUser() {
    return readJson('ka_current_user', payload().current_user || null);
  }

  function setCurrentUser(user) {
    if (!user) {
      return removeKey('ka_current_user');
    }
    localStorage.setItem('ka_current_user', JSON.stringify(user));
    return user;
  }

  function setLoggedIn(flag) {
    const value = flag ? '1' : '0';
    localStorage.setItem('ka_logged_in', value);
    sessionStorage.setItem('ka_logged_in', value);
  }

  function pendingRegistrations() {
    return readJson('ka_pending_registrations', bootstrappedRegistrations());
  }

  function savePendingRegistrations(rows) {
    return writeJson('ka_pending_registrations', rows);
  }

  function addPendingRegistration(user) {
    const rows = pendingRegistrations();
    rows.unshift(user);
    savePendingRegistrations(rows);
    return user;
  }

  function updateRegistration(userId, patch) {
    const rows = pendingRegistrations();
    const next = rows.map(function (row) {
      if (row.id !== userId) return row;
      return Object.assign({}, row, patch || {});
    });
    savePendingRegistrations(next);
    const updated = next.find(function (row) { return row.id === userId; }) || null;
    const current = currentUser();
    if (current && current.id === userId && updated) {
      setCurrentUser(updated);
    }
    return updated;
  }

  function approveRegistration(userId, trackLabel) {
    return updateRegistration(userId, {
      status: 'approved',
      approvedTrack: trackLabel || '',
      approvedAt: new Date().toISOString()
    });
  }

  function rejectRegistration(userId, reason) {
    return updateRegistration(userId, {
      status: 'rejected',
      rejectionReason: reason || '',
      rejectedAt: new Date().toISOString()
    });
  }

  function intakeSubmissions() {
    return readJson('ka_intake_submissions', bootstrappedSubmissions());
  }

  function saveIntakeSubmissions(rows) {
    return writeJson('ka_intake_submissions', rows);
  }

  function addIntakeSubmission(row) {
    const rows = intakeSubmissions();
    rows.unshift(row);
    saveIntakeSubmissions(rows);
    return row;
  }

  function userMetrics(userId) {
    const rows = intakeSubmissions().filter(function (row) {
      return userId ? row.userId === userId : row.identityType === 'anonymous';
    });
    return {
      pending: rows.filter(function (row) { return row.status === 'pending'; }).length,
      approved: rows.filter(function (row) { return row.status === 'approved'; }).length,
      rejected: rows.filter(function (row) { return row.status === 'rejected'; }).length,
      duplicates: rows.filter(function (row) { return row.status === 'duplicate_existing'; }).length,
      rows: rows
    };
  }

  function registrationsByStatus(status) {
    return pendingRegistrations().filter(function (row) {
      return String(row.status || 'pending') === status;
    });
  }

  function allUsers() {
    return pendingRegistrations().slice().sort(function (a, b) {
      return String(b.timestamp || '').localeCompare(String(a.timestamp || ''));
    });
  }

  function trackRoster() {
    const approved = registrationsByStatus('approved');
    const grouped = {};
    approved.forEach(function (row) {
      const key = row.approvedTrack || row.trackChoice1 || 'Unassigned';
      if (!grouped[key]) grouped[key] = [];
      grouped[key].push(row);
    });
    return grouped;
  }

  function trackCapacity() {
    const targetRows = payload().track_targets || [];
    const labels = targetRows.length
      ? targetRows.map(function (row) { return row.track_label; })
      : [
          'Track 1 — Image Tagger',
          'Track 2 — Article Finder',
          'Track 3 — AI & VR',
          'Track 4 — Interaction Design'
        ];
    const targets = {};
    targetRows.forEach(function (row) {
      targets[row.track_label] = row.target;
    });
    const approved = registrationsByStatus('approved');
    return labels.map(function (label) {
      const approvedCount = approved.filter(function (row) {
        return (row.approvedTrack || row.trackChoice1 || '') === label;
      }).length;
      const target = Number(targets[label] || 0);
      return {
        label: label,
        approved: approvedCount,
        target: target,
        pct: target ? Math.min(100, Math.round((approvedCount / target) * 100)) : 0
      };
    });
  }

  function resetToBootstrap() {
    removeKey('ka_pending_registrations');
    removeKey('ka_intake_submissions');
    return {
      registrations: pendingRegistrations(),
      submissions: intakeSubmissions()
    };
  }

  window.KA_WORKFLOW_STORE = {
    payload: payload,
    readJson: readJson,
    writeJson: writeJson,
    currentUser: currentUser,
    setCurrentUser: setCurrentUser,
    setLoggedIn: setLoggedIn,
    pendingRegistrations: pendingRegistrations,
    savePendingRegistrations: savePendingRegistrations,
    addPendingRegistration: addPendingRegistration,
    updateRegistration: updateRegistration,
    approveRegistration: approveRegistration,
    rejectRegistration: rejectRegistration,
    registrationsByStatus: registrationsByStatus,
    allUsers: allUsers,
    trackRoster: trackRoster,
    trackCapacity: trackCapacity,
    intakeSubmissions: intakeSubmissions,
    saveIntakeSubmissions: saveIntakeSubmissions,
    addIntakeSubmission: addIntakeSubmission,
    userMetrics: userMetrics,
    resetToBootstrap: resetToBootstrap
  };
})();
