import { describe, it, expect } from 'vitest';
import { reviewCompliance } from '../src/agents/compliance.js';

describe('compliance agent — static rules', () => {
  it('blocks engineering claims', async () => {
    const r = await reviewCompliance({
      surface: 'listing',
      text: 'These plans are stamped and engineer approved for any climate.',
      has_digital_only_disclosure: true,
      has_personal_use_license: true,
      has_diy_disclaimer: true,
    });
    expect(r.output.pass).toBe(false);
    expect(r.output.blocks.some((b) => /stamped/i.test(b))).toBe(true);
  });

  it('blocks listing missing required disclosures', async () => {
    const r = await reviewCompliance({
      surface: 'listing',
      text: 'A nice plan for your homestead.',
    });
    expect(r.output.pass).toBe(false);
    expect(r.output.blocks).toContain('Listing missing "digital download / no physical product" statement.');
  });

  it('passes well-formed listing copy', async () => {
    const r = await reviewCompliance({
      surface: 'listing',
      text:
        'This is a digital download. No physical product is shipped. Personal use only. Verify your local codes before building.',
      has_digital_only_disclosure: true,
      has_personal_use_license: true,
      has_diy_disclaimer: true,
    });
    expect(r.output.pass).toBe(true);
  });

  it('blocks hero image without DIGITAL PLANS overlay', async () => {
    const r = await reviewCompliance({
      surface: 'image',
      text: '',
      hero_image_says_digital_plans: false,
    });
    expect(r.output.pass).toBe(false);
  });
});
