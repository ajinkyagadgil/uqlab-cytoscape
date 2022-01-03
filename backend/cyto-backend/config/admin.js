module.exports = ({ env }) => ({
  auth: {
    secret: env('ADMIN_JWT_SECRET', '0eb9b99b7b13cd3ed25dc8ea4323891e'),
  },
});
