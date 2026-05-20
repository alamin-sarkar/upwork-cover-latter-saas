"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useEffect, useState } from "react";

import { apiClient, ApiError } from "@/lib/api-client";
import { useSessionStore } from "@/lib/auth-store";
import type { ProfileDetail, ProfilePreferences, ProfileProject, ProfileSkill } from "@/types/api";

async function fetchProfile(token: string) {
  try {
    return await apiClient.get<ProfileDetail>("/profile", { token });
  } catch (error) {
    if (error instanceof ApiError && error.status === 404) {
      return null;
    }
    throw error;
  }
}

export default function SettingsPage() {
  const accessToken = useSessionStore((state) => state.accessToken);
  const queryClient = useQueryClient();
  const [message, setMessage] = useState<string | null>(null);

  const profileQuery = useQuery({
    queryKey: ["profile", "settings"],
    queryFn: () => fetchProfile(accessToken as string),
    enabled: Boolean(accessToken),
  });

  const profile = profileQuery.data;

  const [profileForm, setProfileForm] = useState({
    professional_title: "",
    location: "",
    hourly_rate_usd: "",
    about: "",
    availability_note: "",
  });
  const [preferenceForm, setPreferenceForm] = useState({
    default_tone: "",
    voice_note: "",
    avoid_phrases: "",
    preferred_length: "",
    cta_style: "",
    signature: "",
    extra_instructions: "",
  });
  const [skillForm, setSkillForm] = useState({
    name: "",
    level: "",
    years_of_experience: "",
    proof: "",
  });
  const [projectForm, setProjectForm] = useState({
    title: "",
    role: "",
    tagline: "",
    description: "",
    outcome: "",
    link: "",
    stack: "",
    evidence_points: "",
  });

  useEffect(() => {
    if (!profile) {
      return;
    }
    setProfileForm({
      professional_title: profile.professional_title ?? "",
      location: profile.location ?? "",
      hourly_rate_usd: profile.hourly_rate_usd?.toString() ?? "",
      about: profile.about ?? "",
      availability_note: profile.availability_note ?? "",
    });
    setPreferenceForm({
      default_tone: profile.preferences?.default_tone ?? "",
      voice_note: profile.preferences?.voice_note ?? "",
      avoid_phrases: profile.preferences?.avoid_phrases.join("\n") ?? "",
      preferred_length: profile.preferences?.preferred_length ?? "",
      cta_style: profile.preferences?.cta_style ?? "",
      signature: profile.preferences?.signature ?? "",
      extra_instructions: profile.preferences?.extra_instructions ?? "",
    });
  }, [profile]);

  const saveProfileMutation = useMutation({
    mutationFn: async () => {
      const payload = {
        professional_title: profileForm.professional_title || null,
        location: profileForm.location || null,
        hourly_rate_usd: profileForm.hourly_rate_usd ? Number(profileForm.hourly_rate_usd) : null,
        about: profileForm.about || null,
        availability_note: profileForm.availability_note || null,
      };
      if (profile) {
        return apiClient.patch("/profile", payload, { token: accessToken });
      }
      return apiClient.post("/profile", payload, { token: accessToken });
    },
    onSuccess: async () => {
      setMessage("Profile saved.");
      await queryClient.invalidateQueries({ queryKey: ["profile"] });
    },
  });

  const savePreferencesMutation = useMutation({
    mutationFn: async () => {
      const payload = {
        default_tone: preferenceForm.default_tone || null,
        voice_note: preferenceForm.voice_note || null,
        avoid_phrases: preferenceForm.avoid_phrases
          .split("\n")
          .map((item) => item.trim())
          .filter(Boolean),
        preferred_length: preferenceForm.preferred_length || null,
        cta_style: preferenceForm.cta_style || null,
        signature: preferenceForm.signature || null,
        extra_instructions: preferenceForm.extra_instructions || null,
      };
      if (profile?.preferences) {
        return apiClient.patch<ProfilePreferences>("/profile/preferences", payload, {
          token: accessToken,
        });
      }
      return apiClient.post<ProfilePreferences>("/profile/preferences", payload, {
        token: accessToken,
      });
    },
    onSuccess: async () => {
      setMessage("Preferences saved.");
      await queryClient.invalidateQueries({ queryKey: ["profile"] });
    },
  });

  const createSkillMutation = useMutation({
    mutationFn: () =>
      apiClient.post<ProfileSkill>(
        "/profile/skills",
        {
          name: skillForm.name,
          level: skillForm.level || null,
          years_of_experience: skillForm.years_of_experience
            ? Number(skillForm.years_of_experience)
            : null,
          proof: skillForm.proof || null,
        },
        { token: accessToken },
      ),
    onSuccess: async () => {
      setSkillForm({ name: "", level: "", years_of_experience: "", proof: "" });
      await queryClient.invalidateQueries({ queryKey: ["profile"] });
    },
  });

  const createProjectMutation = useMutation({
    mutationFn: () =>
      apiClient.post<ProfileProject>(
        "/profile/projects",
        {
          title: projectForm.title,
          role: projectForm.role || null,
          tagline: projectForm.tagline || null,
          description: projectForm.description,
          outcome: projectForm.outcome || null,
          link: projectForm.link || null,
          stack: projectForm.stack.split(",").map((item) => item.trim()).filter(Boolean),
          evidence_points: projectForm.evidence_points
            .split("\n")
            .map((item) => item.trim())
            .filter(Boolean),
        },
        { token: accessToken },
      ),
    onSuccess: async () => {
      setProjectForm({
        title: "",
        role: "",
        tagline: "",
        description: "",
        outcome: "",
        link: "",
        stack: "",
        evidence_points: "",
      });
      await queryClient.invalidateQueries({ queryKey: ["profile"] });
    },
  });

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1 className="page-title">Settings</h1>
          <p className="page-subtitle">
            Fill the profile evidence and preferences that generation uses as source material.
          </p>
        </div>
      </div>

      {message ? (
        <div className="card" style={{ marginBottom: 16, padding: 14 }}>
          {message}
        </div>
      ) : null}

      <div className="settings-grid">
        <aside className="settings-side-nav">
          <div className="settings-side-item active">Profile</div>
          <div className="settings-side-item active">Preferences</div>
          <div className="settings-side-item active">Skills</div>
          <div className="settings-side-item active">Projects</div>
        </aside>

        <div className="col" style={{ gap: 20 }}>
          <section className="card">
            <h2 className="card-title" style={{ marginBottom: 16 }}>Profile</h2>
            <div className="grid-2">
              <div className="field">
                <label className="label">Professional title</label>
                <input className="input" value={profileForm.professional_title} onChange={(event) => setProfileForm((current) => ({ ...current, professional_title: event.target.value }))} />
              </div>
              <div className="field">
                <label className="label">Location</label>
                <input className="input" value={profileForm.location} onChange={(event) => setProfileForm((current) => ({ ...current, location: event.target.value }))} />
              </div>
            </div>
            <div className="grid-2">
              <div className="field">
                <label className="label">Hourly rate USD</label>
                <input className="input" value={profileForm.hourly_rate_usd} onChange={(event) => setProfileForm((current) => ({ ...current, hourly_rate_usd: event.target.value }))} />
              </div>
              <div className="field">
                <label className="label">Availability note</label>
                <input className="input" value={profileForm.availability_note} onChange={(event) => setProfileForm((current) => ({ ...current, availability_note: event.target.value }))} />
              </div>
            </div>
            <div className="field">
              <label className="label">About</label>
              <textarea className="textarea" value={profileForm.about} onChange={(event) => setProfileForm((current) => ({ ...current, about: event.target.value }))} />
            </div>
            <button className="btn btn-primary" type="button" onClick={() => saveProfileMutation.mutate()}>
              Save profile
            </button>
          </section>

          <section className="card">
            <h2 className="card-title" style={{ marginBottom: 16 }}>Preferences</h2>
            <div className="grid-2">
              <div className="field">
                <label className="label">Default tone</label>
                <input className="input" value={preferenceForm.default_tone} onChange={(event) => setPreferenceForm((current) => ({ ...current, default_tone: event.target.value }))} />
              </div>
              <div className="field">
                <label className="label">Preferred length</label>
                <input className="input" value={preferenceForm.preferred_length} onChange={(event) => setPreferenceForm((current) => ({ ...current, preferred_length: event.target.value }))} />
              </div>
            </div>
            <div className="grid-2">
              <div className="field">
                <label className="label">CTA style</label>
                <input className="input" value={preferenceForm.cta_style} onChange={(event) => setPreferenceForm((current) => ({ ...current, cta_style: event.target.value }))} />
              </div>
              <div className="field">
                <label className="label">Signature</label>
                <input className="input" value={preferenceForm.signature} onChange={(event) => setPreferenceForm((current) => ({ ...current, signature: event.target.value }))} />
              </div>
            </div>
            <div className="field">
              <label className="label">Voice note</label>
              <textarea className="textarea" value={preferenceForm.voice_note} onChange={(event) => setPreferenceForm((current) => ({ ...current, voice_note: event.target.value }))} />
            </div>
            <div className="field">
              <label className="label">Avoid phrases</label>
              <textarea className="textarea" value={preferenceForm.avoid_phrases} onChange={(event) => setPreferenceForm((current) => ({ ...current, avoid_phrases: event.target.value }))} placeholder="One phrase per line" />
            </div>
            <div className="field">
              <label className="label">Extra instructions</label>
              <textarea className="textarea" value={preferenceForm.extra_instructions} onChange={(event) => setPreferenceForm((current) => ({ ...current, extra_instructions: event.target.value }))} />
            </div>
            <button className="btn btn-primary" type="button" onClick={() => savePreferencesMutation.mutate()}>
              Save preferences
            </button>
          </section>

          <section className="card">
            <h2 className="card-title" style={{ marginBottom: 16 }}>Skills</h2>
            <div className="grid-2">
              <div className="field">
                <label className="label">Skill name</label>
                <input className="input" value={skillForm.name} onChange={(event) => setSkillForm((current) => ({ ...current, name: event.target.value }))} />
              </div>
              <div className="field">
                <label className="label">Level</label>
                <input className="input" value={skillForm.level} onChange={(event) => setSkillForm((current) => ({ ...current, level: event.target.value }))} />
              </div>
            </div>
            <div className="grid-2">
              <div className="field">
                <label className="label">Years of experience</label>
                <input className="input" value={skillForm.years_of_experience} onChange={(event) => setSkillForm((current) => ({ ...current, years_of_experience: event.target.value }))} />
              </div>
              <div className="field">
                <label className="label">Proof</label>
                <input className="input" value={skillForm.proof} onChange={(event) => setSkillForm((current) => ({ ...current, proof: event.target.value }))} />
              </div>
            </div>
            <button className="btn btn-primary" type="button" onClick={() => createSkillMutation.mutate()}>
              Add skill
            </button>
            <div className="row mt-4" style={{ flexWrap: "wrap" }}>
              {(profile?.skills ?? []).map((skill) => (
                <span key={skill.id} className="chip active">
                  {skill.name}{skill.level ? ` · ${skill.level}` : ""}
                </span>
              ))}
            </div>
          </section>

          <section className="card">
            <h2 className="card-title" style={{ marginBottom: 16 }}>Projects</h2>
            <div className="grid-2">
              <div className="field">
                <label className="label">Title</label>
                <input className="input" value={projectForm.title} onChange={(event) => setProjectForm((current) => ({ ...current, title: event.target.value }))} />
              </div>
              <div className="field">
                <label className="label">Role</label>
                <input className="input" value={projectForm.role} onChange={(event) => setProjectForm((current) => ({ ...current, role: event.target.value }))} />
              </div>
            </div>
            <div className="field">
              <label className="label">Tagline</label>
              <input className="input" value={projectForm.tagline} onChange={(event) => setProjectForm((current) => ({ ...current, tagline: event.target.value }))} />
            </div>
            <div className="field">
              <label className="label">Description</label>
              <textarea className="textarea" value={projectForm.description} onChange={(event) => setProjectForm((current) => ({ ...current, description: event.target.value }))} />
            </div>
            <div className="grid-2">
              <div className="field">
                <label className="label">Outcome</label>
                <input className="input" value={projectForm.outcome} onChange={(event) => setProjectForm((current) => ({ ...current, outcome: event.target.value }))} />
              </div>
              <div className="field">
                <label className="label">Link</label>
                <input className="input" value={projectForm.link} onChange={(event) => setProjectForm((current) => ({ ...current, link: event.target.value }))} />
              </div>
            </div>
            <div className="grid-2">
              <div className="field">
                <label className="label">Stack</label>
                <input className="input" value={projectForm.stack} onChange={(event) => setProjectForm((current) => ({ ...current, stack: event.target.value }))} placeholder="Comma separated" />
              </div>
              <div className="field">
                <label className="label">Evidence points</label>
                <textarea className="textarea" value={projectForm.evidence_points} onChange={(event) => setProjectForm((current) => ({ ...current, evidence_points: event.target.value }))} placeholder="One line per proof point" />
              </div>
            </div>
            <button className="btn btn-primary" type="button" onClick={() => createProjectMutation.mutate()}>
              Add project
            </button>

            <div className="col mt-4" style={{ gap: 10 }}>
              {(profile?.projects ?? []).map((project) => (
                <div key={project.id} className="card" style={{ padding: 14 }}>
                  <div style={{ fontWeight: 600 }}>{project.title}</div>
                  <div style={{ fontSize: 12, color: "var(--text-3)", marginBottom: 8 }}>
                    {project.role || "Project"}{project.tagline ? ` · ${project.tagline}` : ""}
                  </div>
                  <div style={{ fontSize: 13, color: "var(--text-2)" }}>{project.description}</div>
                </div>
              ))}
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}
